"""
Data models for the ANTLR4-based SQL lineage system.

Operator ID format:  {ENGINE}_{OP_TYPE}_{SUBTYPE}_{HEX6}
Examples:
    SP_SC_TBL_a1b2c3   (Spark, SCAN, TABLE_SCAN)
    OG_JN_LFT_d4e5f6   (OpenGauss, JOIN, LEFT_JOIN)
    HV_AG_GRP_001234   (Hive, AGGREGATE, GROUP_AGG)
    PG_WR_INS_abcdef   (PostgreSQL, WRITE, INSERT_WRITE)
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# ============================================================
# Engine
# ============================================================


class SqlEngine(str, Enum):
    SPARK = "SPARK"
    HIVE = "HIVE"
    OPENGAUSS = "OPENGAUSS"
    POSTGRESQL = "POSTGRESQL"

    @property
    def prefix(self) -> str:
        _map = {
            "SPARK": "SP",
            "HIVE": "HV",
            "OPENGAUSS": "OG",
            "POSTGRESQL": "PG",
        }
        return _map[self.value]


# ============================================================
# Operator types and subtypes
# ============================================================


class OperatorType(str, Enum):
    SCAN = "SCAN"
    UNNEST = "UNNEST"
    FILTER = "FILTER"
    AGGREGATE = "AGGREGATE"
    WINDOW = "WINDOW"
    JOIN = "JOIN"
    SET = "SET"
    PROJECT = "PROJECT"
    WRITE = "WRITE"

    @property
    def code(self) -> str:
        _map = {
            "SCAN": "SC",
            "UNNEST": "UN",
            "FILTER": "FL",
            "AGGREGATE": "AG",
            "WINDOW": "WN",
            "JOIN": "JN",
            "SET": "ST",
            "PROJECT": "PJ",
            "WRITE": "WR",
        }
        return _map[self.value]


class OperatorSubtype(str, Enum):
    # SCAN subtypes
    TABLE_SCAN = "TABLE_SCAN"
    INDEX_SCAN = "INDEX_SCAN"
    FULL_SCAN = "FULL_SCAN"
    PARTITION_SCAN = "PARTITION_SCAN"
    SAMPLE_SCAN = "SAMPLE_SCAN"
    CTE_SCAN = "CTE_SCAN"
    VALUES_SCAN = "VALUES_SCAN"
    SUBQUERY_SCAN = "SUBQUERY_SCAN"

    # UNNEST subtypes
    LATERAL_VIEW = "LATERAL_VIEW"
    EXPLODE = "EXPLODE"
    POSEXPLODE = "POSEXPLODE"
    INLINE = "INLINE"
    JSON_TABLE = "JSON_TABLE"
    GENERATE_SERIES = "GENERATE_SERIES"
    UNNEST_ORDINALITY = "UNNEST_ORDINALITY"

    # FILTER subtypes
    WHERE_FILTER = "WHERE_FILTER"
    HAVING_FILTER = "HAVING_FILTER"
    QUALIFY_FILTER = "QUALIFY_FILTER"
    ON_FILTER = "ON_FILTER"
    CASE_FILTER = "CASE_FILTER"

    # AGGREGATE subtypes
    GROUP_AGG = "GROUP_AGG"
    DISTINCT_AGG = "DISTINCT_AGG"
    ROLLUP = "ROLLUP"
    CUBE = "CUBE"
    GROUPING_SETS = "GROUPING_SETS"
    STREAMING_AGG = "STREAMING_AGG"
    ORDERED_AGG = "ORDERED_AGG"
    FILTER_AGG = "FILTER_AGG"

    # WINDOW subtypes
    RANK_WINDOW = "RANK_WINDOW"
    VALUE_WINDOW = "VALUE_WINDOW"
    AGGREGATE_WINDOW = "AGGREGATE_WINDOW"
    NTILE_WINDOW = "NTILE_WINDOW"
    FRAME_WINDOW = "FRAME_WINDOW"
    NAMED_WINDOW = "NAMED_WINDOW"

    # JOIN subtypes
    INNER_JOIN = "INNER_JOIN"
    LEFT_JOIN = "LEFT_JOIN"
    RIGHT_JOIN = "RIGHT_JOIN"
    FULL_JOIN = "FULL_JOIN"
    CROSS_JOIN = "CROSS_JOIN"
    SEMI_JOIN = "SEMI_JOIN"
    ANTI_JOIN = "ANTI_JOIN"
    LATERAL_JOIN = "LATERAL_JOIN"
    NATURAL_JOIN = "NATURAL_JOIN"
    SELF_JOIN = "SELF_JOIN"

    # SET subtypes
    UNION = "UNION"
    UNION_ALL = "UNION_ALL"
    INTERSECT = "INTERSECT"
    EXCEPT = "EXCEPT"
    MINUS = "MINUS"

    # PROJECT subtypes
    SELECT_PROJECT = "SELECT_PROJECT"
    EXPRESSION_PROJECT = "EXPRESSION_PROJECT"
    CAST_PROJECT = "CAST_PROJECT"
    ALIAS_PROJECT = "ALIAS_PROJECT"
    STRUCT_PROJECT = "STRUCT_PROJECT"
    TRANSFORM_PROJECT = "TRANSFORM_PROJECT"

    # WRITE subtypes
    INSERT_WRITE = "INSERT_WRITE"
    OVERWRITE_WRITE = "OVERWRITE_WRITE"
    MERGE_WRITE = "MERGE_WRITE"
    CTAS_WRITE = "CTAS_WRITE"
    COPY_WRITE = "COPY_WRITE"
    UPDATE_WRITE = "UPDATE_WRITE"
    DELETE_WRITE = "DELETE_WRITE"
    CREATE_VIEW_WRITE = "CREATE_VIEW_WRITE"
    CREATE_MAT_VIEW_WRITE = "CREATE_MAT_VIEW_WRITE"

    @property
    def code(self) -> str:
        # 3-letter short codes, guaranteed unique across all subtypes
        _map = {
            # SCAN
            "TABLE_SCAN": "TBL",
            "INDEX_SCAN": "IDX",
            "FULL_SCAN": "FUL",
            "PARTITION_SCAN": "PRT",
            "SAMPLE_SCAN": "SMP",
            "CTE_SCAN": "CTE",
            "VALUES_SCAN": "VAL",
            "SUBQUERY_SCAN": "SBQ",
            # UNNEST
            "LATERAL_VIEW": "LTV",
            "EXPLODE": "EXP",
            "POSEXPLODE": "POS",
            "INLINE": "INL",
            "JSON_TABLE": "JST",
            "GENERATE_SERIES": "GEN",
            "UNNEST_ORDINALITY": "ORD",
            # FILTER
            "WHERE_FILTER": "WHR",
            "HAVING_FILTER": "HAV",
            "QUALIFY_FILTER": "QLF",
            "ON_FILTER": "ONF",
            "CASE_FILTER": "CSF",
            # AGGREGATE
            "GROUP_AGG": "GRP",
            "DISTINCT_AGG": "DST",
            "ROLLUP": "RLU",
            "CUBE": "CBE",
            "GROUPING_SETS": "GST",
            "STREAMING_AGG": "STR",
            "ORDERED_AGG": "ORG",
            "FILTER_AGG": "FAG",
            # WINDOW
            "RANK_WINDOW": "RNK",
            "VALUE_WINDOW": "VAW",
            "AGGREGATE_WINDOW": "AWN",
            "NTILE_WINDOW": "NTL",
            "FRAME_WINDOW": "FRM",
            "NAMED_WINDOW": "NMW",
            # JOIN
            "INNER_JOIN": "INR",
            "LEFT_JOIN": "LFT",
            "RIGHT_JOIN": "RGT",
            "FULL_JOIN": "FUJ",
            "CROSS_JOIN": "CRS",
            "SEMI_JOIN": "SMJ",
            "ANTI_JOIN": "ANT",
            "LATERAL_JOIN": "LAT",
            "NATURAL_JOIN": "NAT",
            "SELF_JOIN": "SLF",
            # SET
            "UNION": "UNI",
            "UNION_ALL": "UAL",
            "INTERSECT": "IST",
            "EXCEPT": "EXT",
            "MINUS": "MNS",
            # PROJECT
            "SELECT_PROJECT": "SEL",
            "EXPRESSION_PROJECT": "EPJ",
            "CAST_PROJECT": "CST",
            "ALIAS_PROJECT": "ALS",
            "STRUCT_PROJECT": "STP",
            "TRANSFORM_PROJECT": "TFM",
            # WRITE
            "INSERT_WRITE": "INS",
            "OVERWRITE_WRITE": "OVW",
            "MERGE_WRITE": "MRG",
            "CTAS_WRITE": "CAS",
            "COPY_WRITE": "CPY",
            "UPDATE_WRITE": "UPD",
            "DELETE_WRITE": "DEL",
            "CREATE_VIEW_WRITE": "CVW",
            "CREATE_MAT_VIEW_WRITE": "CMV",
        }
        return _map[self.value]


# ============================================================
# ID generator
# ============================================================


def make_operator_id(
    engine: SqlEngine,
    op_type: OperatorType,
    subtype: OperatorSubtype,
) -> str:
    """Generate a collision-resistant operator ID.

    Format: {ENGINE_PREFIX}_{OP_CODE}_{SUBTYPE_CODE}_{HEX6}
    Example: SP_SC_TBL_a1b2c3
    """
    hex6 = uuid.uuid4().hex[:6]
    return f"{engine.prefix}_{op_type.code}_{subtype.code}_{hex6}"


def make_dataset_id(engine: SqlEngine, schema: str, table: str) -> str:
    hex6 = uuid.uuid4().hex[:6]
    return f"DS_{engine.prefix}_{schema}_{table}_{hex6}".lower()


def make_column_id(dataset_id: str, column_name: str) -> str:
    safe = column_name.replace(" ", "_").lower()
    hex4 = uuid.uuid4().hex[:4]
    return f"{dataset_id}__col_{safe}_{hex4}"


def make_edge_id(from_op: str, to_op: str) -> str:
    hex6 = uuid.uuid4().hex[:6]
    return f"EDGE_{from_op}__{to_op}_{hex6}"


def make_statement_id(engine: SqlEngine) -> str:
    return f"STMT_{engine.prefix}_{uuid.uuid4().hex[:8]}"


# ============================================================
# Core data models
# ============================================================


@dataclass
class ColumnMeta:
    """Column-level metadata with Chinese/English names."""

    id: str
    dataset_id: str
    name_en: str
    name_cn: str
    data_type: str
    nullable: bool = True
    primary_key: bool = False
    comment: str = ""
    ordinal: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "dataset_id": self.dataset_id,
            "name": self.name_en,
            "name_cn": self.name_cn,
            "type": self.data_type,
            "nullable": self.nullable,
            "primary_key": self.primary_key,
            "comment": self.comment,
            "ordinal": self.ordinal,
        }


@dataclass
class DatasetMeta:
    """Table / view / materialized view metadata."""

    id: str
    name: str
    schema: str
    database: str
    engine: SqlEngine
    columns: List[ColumnMeta] = field(default_factory=list)
    primary_keys: List[str] = field(default_factory=list)
    is_partitioned: bool = False
    partition_keys: List[str] = field(default_factory=list)
    comment: str = ""

    @property
    def urn(self) -> str:
        platform = self.engine.value.lower()
        fqn = f"{self.database}.{self.schema}.{self.name}"
        return f"urn:li:dataset:(urn:li:dataPlatform:{platform},{fqn},PROD)"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "urn": self.urn,
            "name": self.name,
            "schema": self.schema,
            "database": self.database,
            "engine": self.engine.value,
            "columns": [c.to_dict() for c in self.columns],
            "primary_keys": self.primary_keys,
            "is_partitioned": self.is_partitioned,
            "partition_keys": self.partition_keys,
            "comment": self.comment,
        }


@dataclass
class OperatorNode:
    """A single operator node in the lineage DAG."""

    id: str
    type: OperatorType
    subtype: OperatorSubtype
    engine: SqlEngine
    # Column IDs this operator consumes
    input_columns: List[str] = field(default_factory=list)
    # Column IDs this operator produces
    output_columns: List[str] = field(default_factory=list)
    # Dataset IDs read by this operator
    input_datasets: List[str] = field(default_factory=list)
    # Dataset IDs written by this operator
    output_datasets: List[str] = field(default_factory=list)
    # Operator-specific properties (expressions, conditions, etc.)
    properties: Dict[str, Any] = field(default_factory=dict)
    # Macro variables referenced by this operator
    macros: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "subtype": self.subtype.value,
            "engine": self.engine.value,
            "input_columns": self.input_columns,
            "output_columns": self.output_columns,
            "input_datasets": self.input_datasets,
            "output_datasets": self.output_datasets,
            "properties": self.properties,
            "macros": self.macros,
        }


@dataclass
class LineageEdge:
    """Directed edge between two operator nodes."""

    id: str
    from_operator_id: str
    to_operator_id: str
    # Fine-grained column mappings: list of (from_col_id, to_col_id)
    column_mappings: List[Dict[str, str]] = field(default_factory=list)
    # Edge classification
    edge_type: str = "DATA_FLOW"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_operator_id": self.from_operator_id,
            "to_operator_id": self.to_operator_id,
            "column_mappings": self.column_mappings,
            "edge_type": self.edge_type,
        }


@dataclass
class StatementMeta:
    """Top-level statement descriptor."""

    id: str
    sql: str
    engine: SqlEngine
    statement_type: str  # SELECT, INSERT, MERGE, CREATE_TABLE, etc.
    # Macro variable name -> default/description
    macros: Dict[str, str] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sql": self.sql,
            "engine": self.engine.value,
            "type": self.statement_type,
            "macros": self.macros,
            "created_at": self.created_at,
        }


@dataclass
class LineageGraph:
    """
    Complete operator-level lineage graph for a single SQL statement.

    Hierarchy:
      statement  -> datasets (tables/views referenced)
                 -> columns  (all columns involved)
                 -> operators (SCAN/FILTER/JOIN/… nodes)
                 -> edges     (data-flow connections between operators)
                 -> lineage   (pre-indexed table/column/statement level)
    """

    statement: StatementMeta
    datasets: List[DatasetMeta] = field(default_factory=list)
    columns: List[ColumnMeta] = field(default_factory=list)
    operators: List[OperatorNode] = field(default_factory=list)
    edges: List[LineageEdge] = field(default_factory=list)

    # ---- Indexes -----------------------------------------------

    @property
    def _dataset_index(self) -> Dict[str, DatasetMeta]:
        return {d.id: d for d in self.datasets}

    @property
    def _column_index(self) -> Dict[str, ColumnMeta]:
        return {c.id: c for c in self.columns}

    @property
    def _operator_index(self) -> Dict[str, OperatorNode]:
        return {op.id: op for op in self.operators}

    # ---- Pre-computed lineage indexes --------------------------

    def _build_table_lineage(self) -> List[Dict[str, Any]]:
        """Build table-level lineage: (source_dataset_urn → target_dataset_urn)."""
        ds_idx = self._dataset_index
        result: List[Dict[str, Any]] = []
        seen: set = set()
        for op in self.operators:
            for src in op.input_datasets:
                for tgt in op.output_datasets:
                    key = (src, tgt)
                    if key not in seen:
                        seen.add(key)
                        src_ds = ds_idx.get(src)
                        tgt_ds = ds_idx.get(tgt)
                        result.append(
                            {
                                "source_dataset_id": src,
                                "source_urn": src_ds.urn if src_ds else src,
                                "target_dataset_id": tgt,
                                "target_urn": tgt_ds.urn if tgt_ds else tgt,
                                "via_operator": op.id,
                            }
                        )
        return result

    def _build_column_lineage(self) -> List[Dict[str, Any]]:
        """Build column-level lineage across all edges."""
        result: List[Dict[str, Any]] = []
        col_idx = self._column_index
        for edge in self.edges:
            for mapping in edge.column_mappings:
                src_col = col_idx.get(mapping.get("from", ""))
                tgt_col = col_idx.get(mapping.get("to", ""))
                result.append(
                    {
                        "source_column_id": mapping.get("from"),
                        "source_column_name": src_col.name_en if src_col else "",
                        "source_dataset_id": src_col.dataset_id if src_col else "",
                        "target_column_id": mapping.get("to"),
                        "target_column_name": tgt_col.name_en if tgt_col else "",
                        "target_dataset_id": tgt_col.dataset_id if tgt_col else "",
                        "via_edge": edge.id,
                        "transform": mapping.get("transform", "PASSTHROUGH"),
                    }
                )
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full lineage graph to a JSON-compatible dictionary."""
        return {
            "version": "1.0",
            "statement": self.statement.to_dict(),
            "datasets": [d.to_dict() for d in self.datasets],
            "columns": [c.to_dict() for c in self.columns],
            "operators": [op.to_dict() for op in self.operators],
            "edges": [e.to_dict() for e in self.edges],
            "lineage": {
                "table_level": self._build_table_lineage(),
                "column_level": self._build_column_lineage(),
                "statement_level": [
                    {
                        "statement_id": self.statement.id,
                        "engine": self.statement.engine.value,
                        "type": self.statement.statement_type,
                        "source_datasets": [
                            ds.id
                            for op in self.operators
                            for ds in [self._dataset_index.get(d) for d in op.input_datasets]
                            if ds
                        ],
                        "target_datasets": [
                            ds.id
                            for op in self.operators
                            for ds in [self._dataset_index.get(d) for d in op.output_datasets]
                            if ds
                        ],
                        "operator_count": len(self.operators),
                        "macro_count": len(self.statement.macros),
                    }
                ],
            },
        }
