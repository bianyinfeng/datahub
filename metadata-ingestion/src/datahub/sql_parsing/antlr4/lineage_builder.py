"""
LineageBuilder — converts a ParsedStatement into an operator-level LineageGraph.

Operator construction follows the logical query plan order:
  SCAN → UNNEST → FILTER → JOIN → AGGREGATE → WINDOW → PROJECT → SET → WRITE

Each operator is assigned a unique ID via make_operator_id().
Edges are created between consecutive operators in the pipeline.
"""

from __future__ import annotations

import datetime
from typing import Dict, List, Optional, Tuple

from datahub.sql_parsing.antlr4.models import (
    ColumnMeta,
    DatasetMeta,
    LineageEdge,
    LineageGraph,
    OperatorNode,
    OperatorSubtype,
    OperatorType,
    SqlEngine,
    StatementMeta,
    make_column_id,
    make_dataset_id,
    make_edge_id,
    make_operator_id,
    make_statement_id,
)
from datahub.sql_parsing.antlr4.parser import ParsedStatement


# ---- Statement type → Write subtype mapping --------------------------

_WRITE_SUBTYPE: Dict[str, OperatorSubtype] = {
    "INSERT": OperatorSubtype.INSERT_WRITE,
    "INSERT_OVERWRITE": OperatorSubtype.OVERWRITE_WRITE,
    "MERGE": OperatorSubtype.MERGE_WRITE,
    "CREATE_TABLE_AS": OperatorSubtype.CTAS_WRITE,
    "CREATE_VIEW": OperatorSubtype.CREATE_VIEW_WRITE,
    "CREATE_MAT_VIEW": OperatorSubtype.CREATE_MAT_VIEW_WRITE,
    "COPY": OperatorSubtype.COPY_WRITE,
    "UPDATE": OperatorSubtype.UPDATE_WRITE,
    "DELETE": OperatorSubtype.DELETE_WRITE,
}

# ---- JOIN type → JOIN subtype mapping --------------------------------

_JOIN_SUBTYPE: Dict[str, OperatorSubtype] = {
    "INNER": OperatorSubtype.INNER_JOIN,
    "LEFT": OperatorSubtype.LEFT_JOIN,
    "LEFT OUTER": OperatorSubtype.LEFT_JOIN,
    "LEFT SEMI": OperatorSubtype.SEMI_JOIN,
    "LEFT ANTI": OperatorSubtype.ANTI_JOIN,
    "ANTI": OperatorSubtype.ANTI_JOIN,
    "SEMI": OperatorSubtype.SEMI_JOIN,
    "RIGHT": OperatorSubtype.RIGHT_JOIN,
    "RIGHT OUTER": OperatorSubtype.RIGHT_JOIN,
    "FULL": OperatorSubtype.FULL_JOIN,
    "FULL OUTER": OperatorSubtype.FULL_JOIN,
    "CROSS": OperatorSubtype.CROSS_JOIN,
    "NATURAL": OperatorSubtype.NATURAL_JOIN,
}


class LineageBuilder:
    """Build a LineageGraph from a ParsedStatement."""

    def __init__(
        self,
        catalog: str = "default_catalog",
        schema_registry: Optional[Dict[str, DatasetMeta]] = None,
    ) -> None:
        self.catalog = catalog
        # Optional pre-loaded metadata registry: "schema.table" → DatasetMeta
        self._registry: Dict[str, DatasetMeta] = schema_registry or {}

    def build(self, parsed: ParsedStatement) -> LineageGraph:
        engine = parsed.engine

        # ---- Statement metadata ------------------------------------
        stmt_meta = StatementMeta(
            id=make_statement_id(engine),
            sql=parsed.sql,
            engine=engine,
            statement_type=parsed.statement_type,
            macros={m.strip("{}"): "" for m in parsed.macros},
            created_at=datetime.datetime.utcnow().isoformat() + "Z",
        )

        graph = LineageGraph(statement=stmt_meta)

        # ---- Resolve datasets --------------------------------------
        all_table_refs = parsed.source_tables + [
            (s, t, "") for s, t in parsed.target_tables
        ]
        # Also include join tables
        for j in parsed.joins:
            all_table_refs.append((j["schema"], j["table"], j.get("alias", "")))

        ds_map: Dict[Tuple[str, str], DatasetMeta] = {}
        for schema, table, _alias in all_table_refs:
            key = (schema, table)
            if key not in ds_map:
                ds = self._resolve_dataset(schema, table, engine)
                ds_map[key] = ds
                graph.datasets.append(ds)
                graph.columns.extend(ds.columns)

        # ---- Helper: get dataset by schema.table -------------------
        def get_ds(schema: str, table: str) -> Optional[DatasetMeta]:
            return ds_map.get((schema, table))

        # ---- SCAN operators ----------------------------------------
        scan_ops: List[OperatorNode] = []
        for schema, table, _alias in parsed.source_tables:
            ds = get_ds(schema, table)
            if ds is None:
                continue
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.SCAN, OperatorSubtype.TABLE_SCAN),
                type=OperatorType.SCAN,
                subtype=OperatorSubtype.TABLE_SCAN,
                engine=engine,
                input_datasets=[ds.id],
                output_columns=[c.id for c in ds.columns],
                properties={"table": f"{schema}.{table}"},
                macros=[m for m in parsed.macros if m.strip("{}") in table or m.strip("{}") in schema],
            )
            scan_ops.append(op)
            graph.operators.append(op)

        # CTE scans
        for cte_name in parsed.ctes:
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.SCAN, OperatorSubtype.CTE_SCAN),
                type=OperatorType.SCAN,
                subtype=OperatorSubtype.CTE_SCAN,
                engine=engine,
                properties={"cte_name": cte_name},
                macros=parsed.macros,
            )
            scan_ops.append(op)
            graph.operators.append(op)

        # ---- UNNEST operators --------------------------------------
        unnest_ops: List[OperatorNode] = []
        for u in parsed.unnests:
            utype = u.get("type", "UNNEST")
            subtype = (
                OperatorSubtype.LATERAL_VIEW
                if utype == "LATERAL_VIEW"
                else OperatorSubtype.EXPLODE
                if "EXPLODE" in u.get("function", "").upper()
                else OperatorSubtype.UNNEST_ORDINALITY
                if "ORDINALITY" in u.get("args", "").upper()
                else OperatorSubtype.EXPLODE
            )
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.UNNEST, subtype),
                type=OperatorType.UNNEST,
                subtype=subtype,
                engine=engine,
                properties=u,
                macros=parsed.macros,
            )
            unnest_ops.append(op)
            graph.operators.append(op)

        # ---- FILTER operators --------------------------------------
        filter_ops: List[OperatorNode] = []
        for f in parsed.filters:
            subtype = (
                OperatorSubtype.WHERE_FILTER
                if f["type"] == "WHERE"
                else OperatorSubtype.HAVING_FILTER
            )
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.FILTER, subtype),
                type=OperatorType.FILTER,
                subtype=subtype,
                engine=engine,
                properties={"condition": f["condition"][:300]},
                macros=parsed.macros,
            )
            filter_ops.append(op)
            graph.operators.append(op)

        # ---- JOIN operators ----------------------------------------
        join_ops: List[OperatorNode] = []
        for j in parsed.joins:
            jkey = j["type"].upper()
            subtype = _JOIN_SUBTYPE.get(jkey, OperatorSubtype.INNER_JOIN)
            ds = get_ds(j["schema"], j["table"])
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.JOIN, subtype),
                type=OperatorType.JOIN,
                subtype=subtype,
                engine=engine,
                input_datasets=[ds.id] if ds else [],
                input_columns=[c.id for c in ds.columns] if ds else [],
                properties={
                    "join_type": j["type"],
                    "table": f"{j['schema']}.{j['table']}",
                    "alias": j.get("alias", ""),
                    "condition": j.get("condition", "")[:300],
                },
                macros=parsed.macros,
            )
            join_ops.append(op)
            graph.operators.append(op)

        # ---- AGGREGATE operators -----------------------------------
        agg_ops: List[OperatorNode] = []
        if parsed.group_by:
            subtype = OperatorSubtype.GROUP_AGG
            # Detect ROLLUP / CUBE / GROUPING SETS
            gb_str = " ".join(parsed.group_by).upper()
            if "ROLLUP" in gb_str:
                subtype = OperatorSubtype.ROLLUP
            elif "CUBE" in gb_str:
                subtype = OperatorSubtype.CUBE
            elif "GROUPING" in gb_str and "SETS" in gb_str:
                subtype = OperatorSubtype.GROUPING_SETS
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.AGGREGATE, subtype),
                type=OperatorType.AGGREGATE,
                subtype=subtype,
                engine=engine,
                properties={"group_by": parsed.group_by[:20]},
                macros=parsed.macros,
            )
            agg_ops.append(op)
            graph.operators.append(op)

        # ---- WINDOW operators --------------------------------------
        window_ops: List[OperatorNode] = []
        for w in parsed.windows:
            func_name = w.get("function", "").upper()
            if func_name in ("RANK", "DENSE_RANK", "ROW_NUMBER", "PERCENT_RANK", "CUME_DIST"):
                subtype = OperatorSubtype.RANK_WINDOW
            elif func_name in ("LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE"):
                subtype = OperatorSubtype.VALUE_WINDOW
            elif func_name == "NTILE":
                subtype = OperatorSubtype.NTILE_WINDOW
            else:
                subtype = OperatorSubtype.AGGREGATE_WINDOW
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.WINDOW, subtype),
                type=OperatorType.WINDOW,
                subtype=subtype,
                engine=engine,
                properties=w,
                macros=parsed.macros,
            )
            window_ops.append(op)
            graph.operators.append(op)

        # ---- SET operators -----------------------------------------
        set_ops: List[OperatorNode] = []
        for set_op_type, _ in parsed.set_ops:
            stype_map = {
                "UNION ALL": OperatorSubtype.UNION_ALL,
                "UNION": OperatorSubtype.UNION,
                "INTERSECT": OperatorSubtype.INTERSECT,
                "EXCEPT": OperatorSubtype.EXCEPT,
                "MINUS": OperatorSubtype.MINUS,
            }
            subtype = stype_map.get(set_op_type, OperatorSubtype.UNION_ALL)
            op = OperatorNode(
                id=make_operator_id(engine, OperatorType.SET, subtype),
                type=OperatorType.SET,
                subtype=subtype,
                engine=engine,
                properties={"operator": set_op_type},
                macros=parsed.macros,
            )
            set_ops.append(op)
            graph.operators.append(op)

        # ---- PROJECT operator ---------------------------------------
        project_subtype = OperatorSubtype.SELECT_PROJECT
        # Detect special project types
        has_cast = any("CAST" in p[0].upper() or "::" in p[0] for p in parsed.projections)
        has_alias = any(p[1] for p in parsed.projections)
        if has_cast:
            project_subtype = OperatorSubtype.CAST_PROJECT
        elif has_alias:
            project_subtype = OperatorSubtype.ALIAS_PROJECT

        # Determine output columns for projection
        all_source_cols: List[str] = []
        for ds in graph.datasets:
            if (ds.schema, ds.name) in [(s, t) for s, t, _ in parsed.source_tables]:
                all_source_cols.extend(c.id for c in ds.columns)

        proj_output_cols: List[ColumnMeta] = []
        for expr, alias in parsed.projections[:50]:  # cap
            col_name = alias or expr.strip()[:60]
            if col_name in ("*", "") or col_name.startswith("*"):
                continue
            # Try to find existing column
            found = None
            for ds in graph.datasets:
                for c in ds.columns:
                    if c.name_en.lower() == col_name.lower():
                        found = c
                        break
            if found is None:
                # Create synthetic projected column
                first_ds = graph.datasets[0] if graph.datasets else None
                ds_id = first_ds.id if first_ds else "unknown"
                col_id = make_column_id(ds_id, col_name)
                found = ColumnMeta(
                    id=col_id,
                    dataset_id=ds_id,
                    name_en=col_name,
                    name_cn=col_name,
                    data_type="UNKNOWN",
                )
                graph.columns.append(found)
            proj_output_cols.append(found)

        project_op = OperatorNode(
            id=make_operator_id(engine, OperatorType.PROJECT, project_subtype),
            type=OperatorType.PROJECT,
            subtype=project_subtype,
            engine=engine,
            input_columns=all_source_cols[:100],
            output_columns=[c.id for c in proj_output_cols],
            properties={
                "projection_count": len(parsed.projections),
                "has_star": any(p[0].strip() == "*" for p in parsed.projections),
            },
            macros=parsed.macros,
        )
        graph.operators.append(project_op)

        # ---- WRITE operator (if applicable) ------------------------
        write_op: Optional[OperatorNode] = None
        if parsed.statement_type in _WRITE_SUBTYPE:
            write_subtype = _WRITE_SUBTYPE[parsed.statement_type]
            tgt_ds_ids: List[str] = []
            for schema, table in parsed.target_tables:
                ds = get_ds(schema, table)
                if ds:
                    tgt_ds_ids.append(ds.id)
                    # Ensure target dataset is in graph
                    if ds not in graph.datasets:
                        graph.datasets.append(ds)
                        graph.columns.extend(ds.columns)
            write_op = OperatorNode(
                id=make_operator_id(engine, OperatorType.WRITE, write_subtype),
                type=OperatorType.WRITE,
                subtype=write_subtype,
                engine=engine,
                input_columns=[c.id for c in proj_output_cols],
                output_datasets=tgt_ds_ids,
                properties={
                    "target_tables": [f"{s}.{t}" for s, t in parsed.target_tables],
                    "partition_cols": parsed.partition_cols,
                },
                macros=parsed.macros,
            )
            graph.operators.append(write_op)

        # Attach dataset IDs to SCAN ops
        for op in scan_ops:
            if op.input_datasets:
                ds_id = op.input_datasets[0]
                # Mark that this scan reads from the dataset
                pass  # already set above

        # Attach target datasets to WRITE op and update SCAN source datasets
        for op in scan_ops:
            for ds in op.input_datasets:
                if write_op and ds not in write_op.input_datasets:
                    pass  # lineage tracked through edges

        # ---- Build edges -------------------------------------------
        # Chain: SCAN → [UNNEST] → [FILTER] → [JOIN] → [AGG] → [WINDOW] → [SET] → PROJECT → [WRITE]

        # Connect SCANs to first processing stage
        all_ops_in_order: List[OperatorNode] = (
            scan_ops + unnest_ops + filter_ops + join_ops + agg_ops + window_ops + set_ops + [project_op]
        )
        if write_op:
            all_ops_in_order.append(write_op)

        prev_ops: List[OperatorNode] = scan_ops if scan_ops else []

        def connect(from_ops: List[OperatorNode], to_op: OperatorNode) -> None:
            for from_op in from_ops:
                edge = LineageEdge(
                    id=make_edge_id(from_op.id, to_op.id),
                    from_operator_id=from_op.id,
                    to_operator_id=to_op.id,
                    column_mappings=self._build_column_mappings(from_op, to_op),
                    edge_type="DATA_FLOW",
                )
                graph.edges.append(edge)

        for stage_ops in [unnest_ops, filter_ops, join_ops, agg_ops, window_ops, set_ops]:
            if stage_ops:
                if prev_ops:
                    for stage_op in stage_ops:
                        connect(prev_ops, stage_op)
                prev_ops = stage_ops

        # Connect to PROJECT
        if prev_ops:
            connect(prev_ops, project_op)

        # Connect PROJECT to WRITE
        if write_op:
            connect([project_op], write_op)

        # Set write target datasets in project_op output (for table-level lineage)
        if write_op:
            project_op.output_datasets = write_op.output_datasets[:]

        # Set scan input datasets to enable table-level lineage
        for op in scan_ops:
            if op.input_datasets:
                # propagate source datasets all the way to write
                if write_op:
                    write_op.input_datasets = list(
                        set(write_op.input_datasets + op.input_datasets)
                    )

        return graph

    def _build_column_mappings(
        self, from_op: OperatorNode, to_op: OperatorNode
    ) -> List[Dict[str, str]]:
        """Build column-level mappings between adjacent operators."""
        mappings: List[Dict[str, str]] = []
        # Match output columns of from_op to input columns of to_op
        from_cols = set(from_op.output_columns)
        to_cols = set(to_op.input_columns)
        for col_id in from_cols & to_cols:
            mappings.append({"from": col_id, "to": col_id, "transform": "PASSTHROUGH"})
        return mappings

    def _resolve_dataset(
        self, schema: str, table: str, engine: SqlEngine
    ) -> DatasetMeta:
        """Look up or create a DatasetMeta for schema.table."""
        key = f"{schema}.{table}"
        if key in self._registry:
            return self._registry[key]

        ds_id = make_dataset_id(engine, schema, table)
        ds = DatasetMeta(
            id=ds_id,
            name=table,
            schema=schema,
            database=self.catalog,
            engine=engine,
        )
        # Synthesize placeholder columns (actual metadata injected via registry)
        for i, col_name in enumerate(["id", "created_at", "updated_at"]):
            col_id = make_column_id(ds_id, col_name)
            col = ColumnMeta(
                id=col_id,
                dataset_id=ds_id,
                name_en=col_name,
                name_cn=col_name,
                data_type="VARCHAR",
                primary_key=(col_name == "id"),
                ordinal=i,
            )
            ds.columns.append(col)
            if col_name == "id":
                ds.primary_keys.append(col_name)

        self._registry[key] = ds
        return ds
