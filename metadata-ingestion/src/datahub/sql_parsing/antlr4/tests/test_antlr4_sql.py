"""
Unit tests for the ANTLR4-based SQL parsing toolkit.

Tests cover:
- Statement type detection
- Macro variable extraction
- Table reference extraction (source / target / CTE)
- JOIN extraction and subtype mapping
- Filter / GROUP BY extraction
- Window function detection
- UNNEST / LATERAL VIEW extraction
- SET operation detection
- LineageGraph construction
- Operator ID uniqueness
- JSON serialization roundtrip
- End-to-end parsing of Spark and OpenGauss corpus files
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List

import pytest

from datahub.sql_parsing.antlr4.models import (
    ColumnMeta,
    DatasetMeta,
    LineageGraph,
    OperatorSubtype,
    OperatorType,
    SqlEngine,
    make_column_id,
    make_dataset_id,
    make_edge_id,
    make_operator_id,
    make_statement_id,
)
from datahub.sql_parsing.antlr4.parser import SqlParser
from datahub.sql_parsing.antlr4.lineage_builder import LineageBuilder

# ------------------------------------------------------------------ #
# Paths                                                                #
# ------------------------------------------------------------------ #

_BASE = Path(__file__).parent.parent
SPARK_CORPUS = _BASE / "corpus" / "spark"
OG_CORPUS = _BASE / "corpus" / "opengauss"
META_DIR = _BASE / "metadata"

# ================================================================== #
# 1. Operator ID generation                                            #
# ================================================================== #


class TestOperatorIdGeneration:
    def test_id_format(self) -> None:
        op_id = make_operator_id(SqlEngine.SPARK, OperatorType.SCAN, OperatorSubtype.TABLE_SCAN)
        parts = op_id.split("_")
        assert parts[0] == "SP", f"Engine prefix wrong: {op_id}"
        assert parts[1] == "SC", f"Op-type code wrong: {op_id}"
        assert parts[2] == "TBL", f"Subtype code wrong: {op_id}"
        assert len(parts[3]) == 6, f"Hex suffix wrong length: {op_id}"
        assert re.fullmatch(r"[0-9a-f]{6}", parts[3]), f"Hex suffix not hex: {op_id}"

    def test_all_engine_prefixes(self) -> None:
        expected = {"SPARK": "SP", "HIVE": "HV", "OPENGAUSS": "OG", "POSTGRESQL": "PG"}
        for name, prefix in expected.items():
            engine = SqlEngine(name)
            op_id = make_operator_id(engine, OperatorType.JOIN, OperatorSubtype.LEFT_JOIN)
            assert op_id.startswith(f"{prefix}_"), f"Wrong prefix for {name}: {op_id}"

    def test_no_collisions_bulk(self) -> None:
        ids: List[str] = []
        for engine in SqlEngine:
            for op_type in OperatorType:
                for subtype in OperatorSubtype:
                    # Each call produces a different suffix
                    ids.append(make_operator_id(engine, op_type, subtype))
        # Structural uniqueness: same (engine, type, subtype) → same deterministic prefix
        # But random suffix ensures no collision across calls
        assert len(ids) == len(set(ids))

    def test_subtype_codes_unique(self) -> None:
        """Each OperatorSubtype must have a unique 3-letter code."""
        codes = [s.code for s in OperatorSubtype]
        assert len(codes) == len(set(codes)), f"Duplicate subtype codes: {codes}"

    def test_optype_codes_unique(self) -> None:
        codes = [t.code for t in OperatorType]
        assert len(codes) == len(set(codes)), f"Duplicate op-type codes: {codes}"

    def test_dataset_id_format(self) -> None:
        ds_id = make_dataset_id(SqlEngine.OPENGAUSS, "dwd", "orders")
        assert "og" in ds_id
        assert "orders" in ds_id

    def test_column_id_contains_name(self) -> None:
        col_id = make_column_id("ds_sp_abc", "user_id")
        assert "user_id" in col_id

    def test_statement_id_prefix(self) -> None:
        stmt_id = make_statement_id(SqlEngine.SPARK)
        assert stmt_id.startswith("STMT_SP_")
        assert len(stmt_id) == len("STMT_SP_") + 8


# ================================================================== #
# 2. Parser — statement type detection                                 #
# ================================================================== #


class TestParserStatementType:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_select(self) -> None:
        assert self.parser.parse("SELECT * FROM t").statement_type == "SELECT"

    def test_cte_select(self) -> None:
        sql = "WITH cte AS (SELECT 1) SELECT * FROM cte"
        assert self.parser.parse(sql).statement_type == "SELECT"

    def test_insert_into(self) -> None:
        sql = "INSERT INTO dwd.orders SELECT * FROM ods.raw_orders"
        assert self.parser.parse(sql).statement_type == "INSERT"

    def test_insert_overwrite(self) -> None:
        sql = "INSERT OVERWRITE TABLE dwd.orders SELECT * FROM ods.raw_orders"
        assert self.parser.parse(sql).statement_type == "INSERT_OVERWRITE"

    def test_merge(self) -> None:
        sql = "MERGE INTO target USING source ON target.id = source.id WHEN MATCHED THEN UPDATE SET x=1"
        assert self.parser.parse(sql).statement_type == "MERGE"

    def test_ctas(self) -> None:
        sql = "CREATE TABLE t USING delta AS SELECT * FROM s"
        assert self.parser.parse(sql).statement_type == "CREATE_TABLE_AS"

    def test_create_view(self) -> None:
        sql = "CREATE OR REPLACE VIEW v AS SELECT * FROM t"
        assert self.parser.parse(sql).statement_type == "CREATE_VIEW"

    def test_create_mat_view(self) -> None:
        sql = "CREATE MATERIALIZED VIEW mv AS SELECT * FROM t"
        pg_parser = SqlParser(engine=SqlEngine.OPENGAUSS)
        assert pg_parser.parse(sql).statement_type == "CREATE_MAT_VIEW"

    def test_copy(self) -> None:
        sql = "COPY dwd.orders FROM '/data/orders.csv'"
        og_parser = SqlParser(engine=SqlEngine.OPENGAUSS)
        assert og_parser.parse(sql).statement_type == "COPY"


# ================================================================== #
# 3. Parser — macro variable extraction                                #
# ================================================================== #


class TestMacroExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_single_macro(self) -> None:
        sql = "SELECT * FROM t WHERE dt = {report_date}"
        parsed = self.parser.parse(sql)
        assert "{report_date}" in parsed.macros

    def test_multiple_macros(self) -> None:
        sql = "INSERT INTO {target_table} SELECT {col1}, {col2} FROM {source_table} WHERE {filter}"
        parsed = self.parser.parse(sql)
        for macro in ["{target_table}", "{col1}", "{col2}", "{source_table}", "{filter}"]:
            assert macro in parsed.macros, f"Missing macro: {macro}"

    def test_no_macros(self) -> None:
        sql = "SELECT user_id FROM dwd.users"
        assert self.parser.parse(sql).macros == []

    def test_macro_in_table_name(self) -> None:
        sql = "SELECT * FROM {schema_name}.{table_name}"
        parsed = self.parser.parse(sql)
        assert "{schema_name}" in parsed.macros
        assert "{table_name}" in parsed.macros

    def test_macro_chinese_name(self) -> None:
        sql = "SELECT * FROM t WHERE region = {目标区域}"
        parsed = self.parser.parse(sql)
        assert "{目标区域}" in parsed.macros


# ================================================================== #
# 4. Parser — table reference extraction                               #
# ================================================================== #


class TestTableExtraction:
    def setup_method(self) -> None:
        self.sp = SqlParser(engine=SqlEngine.SPARK)
        self.og = SqlParser(engine=SqlEngine.OPENGAUSS)

    def test_simple_from(self) -> None:
        parsed = self.sp.parse("SELECT * FROM ods.orders")
        tables = [(s, t) for s, t, _ in parsed.source_tables]
        assert ("ods", "orders") in tables

    def test_insert_target(self) -> None:
        sql = "INSERT INTO dwd.orders SELECT * FROM ods.raw_orders"
        parsed = self.sp.parse(sql)
        assert ("dwd", "orders") in parsed.target_tables
        assert any(t == "raw_orders" for _, t, _ in parsed.source_tables)

    def test_insert_overwrite_target(self) -> None:
        sql = "INSERT OVERWRITE TABLE ads.report PARTITION (dt='2024-01-01') SELECT 1"
        parsed = self.sp.parse(sql)
        assert ("ads", "report") in parsed.target_tables

    def test_cte_not_in_source(self) -> None:
        sql = """
        WITH cte AS (SELECT * FROM ods.orders)
        SELECT * FROM cte
        """
        parsed = self.sp.parse(sql)
        assert "cte" in parsed.ctes
        # cte should not appear as a source table
        source_names = [t for _, t, _ in parsed.source_tables]
        assert "cte" not in source_names

    def test_multi_table_join(self) -> None:
        sql = """
        SELECT o.*, u.name FROM dwd.orders o
        JOIN dwd.user_profile u ON o.user_id = u.user_id
        WHERE o.dt = '2024-01-01'
        """
        parsed = self.sp.parse(sql)
        source_names = {t for _, t, _ in parsed.source_tables}
        assert "orders" in source_names

    def test_merge_target_and_source(self) -> None:
        sql = """
        MERGE INTO dwd.users AS t
        USING staging.user_updates AS s
        ON t.user_id = s.user_id
        WHEN MATCHED THEN UPDATE SET t.name = s.name
        """
        parsed = self.sp.parse(sql)
        assert ("dwd", "users") in parsed.target_tables
        assert any("user_updates" in t for _, t, _ in parsed.source_tables)


# ================================================================== #
# 5. Parser — JOIN extraction                                          #
# ================================================================== #


class TestJoinExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_inner_join(self) -> None:
        sql = "SELECT * FROM a JOIN b ON a.id = b.id"
        joins = self.parser.parse(sql).joins
        assert any(j["table"] == "b" for j in joins)

    def test_left_join(self) -> None:
        sql = "SELECT * FROM a LEFT JOIN b ON a.id = b.id"
        joins = self.parser.parse(sql).joins
        j = next(j for j in joins if j["table"] == "b")
        assert "LEFT" in j["type"].upper()

    def test_multiple_joins(self) -> None:
        sql = """
        SELECT * FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN products p ON o.product_id = p.product_id
        CROSS JOIN dim.regions r
        """
        joins = self.parser.parse(sql).joins
        assert len(joins) >= 2


# ================================================================== #
# 6. Parser — GROUP BY extraction                                      #
# ================================================================== #


class TestGroupByExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_simple_group_by(self) -> None:
        sql = "SELECT user_id, COUNT(*) FROM orders GROUP BY user_id"
        parsed = self.parser.parse(sql)
        assert "user_id" in parsed.group_by

    def test_multi_column_group_by(self) -> None:
        sql = "SELECT a, b, SUM(c) FROM t GROUP BY a, b"
        parsed = self.parser.parse(sql)
        assert "a" in parsed.group_by
        assert "b" in parsed.group_by

    def test_no_group_by(self) -> None:
        assert self.parser.parse("SELECT * FROM t").group_by == []


# ================================================================== #
# 7. Parser — window function detection                                #
# ================================================================== #


class TestWindowExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_rank_window(self) -> None:
        sql = "SELECT RANK() OVER (PARTITION BY user_id ORDER BY amt DESC) FROM t"
        parsed = self.parser.parse(sql)
        assert any(w["function"].upper() == "RANK" for w in parsed.windows)

    def test_multiple_windows(self) -> None:
        sql = """
        SELECT
            ROW_NUMBER() OVER (PARTITION BY a ORDER BY b) AS rn,
            SUM(x) OVER (PARTITION BY a) AS total
        FROM t
        """
        parsed = self.parser.parse(sql)
        assert len(parsed.windows) >= 1


# ================================================================== #
# 8. Parser — UNNEST / LATERAL VIEW                                    #
# ================================================================== #


class TestUnnestExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_lateral_view_explode(self) -> None:
        sql = "SELECT t.*, tag FROM t LATERAL VIEW EXPLODE(tags) tags_table AS tag"
        parsed = self.parser.parse(sql)
        assert len(parsed.unnests) >= 1
        assert parsed.unnests[0]["type"] == "LATERAL_VIEW"

    def test_unnest_opengauss(self) -> None:
        og = SqlParser(engine=SqlEngine.OPENGAUSS)
        sql = "SELECT user_id, t FROM orders CROSS JOIN UNNEST(tags) AS t(tag)"
        parsed = og.parse(sql)
        assert len(parsed.unnests) >= 1


# ================================================================== #
# 9. Parser — SET operations                                           #
# ================================================================== #


class TestSetOpExtraction:
    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)

    def test_union_all(self) -> None:
        sql = "SELECT a FROM t1 UNION ALL SELECT a FROM t2"
        ops = [op for op, _ in self.parser.parse(sql).set_ops]
        assert "UNION ALL" in ops

    def test_intersect(self) -> None:
        sql = "SELECT a FROM t1 INTERSECT SELECT a FROM t2"
        ops = [op for op, _ in self.parser.parse(sql).set_ops]
        assert "INTERSECT" in ops

    def test_except(self) -> None:
        sql = "SELECT a FROM t1 EXCEPT SELECT a FROM t2"
        ops = [op for op, _ in self.parser.parse(sql).set_ops]
        assert "EXCEPT" in ops

    def test_minus(self) -> None:
        sql = "SELECT a FROM t1 MINUS SELECT a FROM t2"
        ops = [op for op, _ in self.parser.parse(sql).set_ops]
        assert "MINUS" in ops


# ================================================================== #
# 10. LineageBuilder — graph construction                              #
# ================================================================== #


class TestLineageBuilder:
    def _build(self, sql: str, engine: SqlEngine = SqlEngine.SPARK) -> LineageGraph:
        parser = SqlParser(engine=engine)
        builder = LineageBuilder()
        return builder.build(parser.parse(sql))

    def test_simple_select_has_scan_and_project(self) -> None:
        graph = self._build("SELECT user_id, order_id FROM ods.orders WHERE dt='2024-01-01'")
        types = {op.type for op in graph.operators}
        assert OperatorType.SCAN in types
        assert OperatorType.PROJECT in types

    def test_insert_has_write_operator(self) -> None:
        sql = "INSERT INTO dwd.orders SELECT * FROM ods.raw_orders"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.WRITE in types

    def test_merge_has_merge_write(self) -> None:
        sql = """
        MERGE INTO dwd.users AS t
        USING staging.users AS s ON t.id = s.id
        WHEN MATCHED THEN UPDATE SET t.name = s.name
        """
        graph = self._build(sql)
        write_ops = [op for op in graph.operators if op.type == OperatorType.WRITE]
        assert len(write_ops) >= 1
        assert any(op.subtype == OperatorSubtype.MERGE_WRITE for op in write_ops)

    def test_join_operator_created(self) -> None:
        sql = "SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.JOIN in types

    def test_filter_operator_created(self) -> None:
        sql = "SELECT * FROM orders WHERE order_status = 'PAID'"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.FILTER in types

    def test_aggregate_operator_created(self) -> None:
        sql = "SELECT user_id, COUNT(*) AS cnt FROM orders GROUP BY user_id"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.AGGREGATE in types

    def test_window_operator_created(self) -> None:
        sql = "SELECT RANK() OVER (PARTITION BY user_id ORDER BY amt DESC) AS rnk FROM orders"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.WINDOW in types

    def test_set_operator_created(self) -> None:
        sql = "SELECT a FROM t1 UNION ALL SELECT a FROM t2"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.SET in types

    def test_unnest_operator_created(self) -> None:
        sql = "SELECT tag FROM products LATERAL VIEW EXPLODE(tags) tbl AS tag"
        graph = self._build(sql)
        types = {op.type for op in graph.operators}
        assert OperatorType.UNNEST in types

    def test_ctas_has_ctas_write(self) -> None:
        sql = "CREATE TABLE dwd.t USING delta AS SELECT * FROM ods.raw"
        graph = self._build(sql)
        write_ops = [op for op in graph.operators if op.type == OperatorType.WRITE]
        assert any(op.subtype == OperatorSubtype.CTAS_WRITE for op in write_ops)

    def test_opengauss_copy_write(self) -> None:
        sql = "COPY ods.orders FROM '/data/orders.csv' WITH (FORMAT CSV)"
        graph = self._build(sql, engine=SqlEngine.OPENGAUSS)
        types = {op.type for op in graph.operators}
        assert OperatorType.WRITE in types

    def test_edges_connect_operators(self) -> None:
        sql = """
        INSERT INTO dwd.orders
        SELECT o.*, u.name FROM ods.raw_orders o
        JOIN dim.users u ON o.user_id = u.user_id
        WHERE o.status = 'PAID'
        GROUP BY o.order_id, u.name
        """
        graph = self._build(sql)
        assert len(graph.edges) >= 1

    def test_edge_ids_unique(self) -> None:
        sql = """
        SELECT * FROM a
        JOIN b ON a.id = b.id
        LEFT JOIN c ON b.x = c.x
        WHERE a.dt = '2024-01-01'
        GROUP BY a.user_id
        """
        graph = self._build(sql)
        edge_ids = [e.id for e in graph.edges]
        assert len(edge_ids) == len(set(edge_ids))

    def test_datasets_populated(self) -> None:
        sql = "SELECT * FROM ods.orders o JOIN dim.users u ON o.user_id = u.user_id"
        graph = self._build(sql)
        assert len(graph.datasets) >= 1

    def test_macros_in_statement_meta(self) -> None:
        sql = "SELECT * FROM {source_table} WHERE dt = {dt}"
        graph = self._build(sql)
        assert len(graph.statement.macros) >= 1


# ================================================================== #
# 11. LineageGraph — JSON serialization                                #
# ================================================================== #


class TestLineageGraphJson:
    def _build_graph(self, sql: str, engine: SqlEngine = SqlEngine.SPARK) -> LineageGraph:
        parser = SqlParser(engine=engine)
        builder = LineageBuilder()
        return builder.build(parser.parse(sql))

    def test_to_dict_has_all_top_level_keys(self) -> None:
        graph = self._build_graph("SELECT user_id FROM ods.orders")
        d = graph.to_dict()
        for key in ["version", "statement", "datasets", "columns", "operators", "edges", "lineage"]:
            assert key in d, f"Missing key: {key}"

    def test_version_is_1_0(self) -> None:
        d = self._build_graph("SELECT 1").to_dict()
        assert d["version"] == "1.0"

    def test_statement_has_required_fields(self) -> None:
        d = self._build_graph("SELECT * FROM t WHERE x=1").to_dict()
        s = d["statement"]
        for field in ["id", "sql", "engine", "type", "macros", "created_at"]:
            assert field in s, f"Statement missing: {field}"

    def test_operators_have_required_fields(self) -> None:
        d = self._build_graph("INSERT INTO dst SELECT * FROM src").to_dict()
        for op in d["operators"]:
            for field in ["id", "type", "subtype", "engine"]:
                assert field in op, f"Operator missing: {field}"

    def test_edges_have_required_fields(self) -> None:
        sql = "SELECT * FROM a JOIN b ON a.id = b.id WHERE a.x > 0"
        d = self._build_graph(sql).to_dict()
        for edge in d["edges"]:
            for field in ["id", "from_operator_id", "to_operator_id"]:
                assert field in edge

    def test_lineage_has_three_levels(self) -> None:
        sql = "INSERT INTO dwd.orders SELECT * FROM ods.raw_orders"
        d = self._build_graph(sql).to_dict()
        lineage = d["lineage"]
        for level in ["table_level", "column_level", "statement_level"]:
            assert level in lineage

    def test_json_roundtrip(self) -> None:
        sql = "SELECT user_id, SUM(amount) FROM orders GROUP BY user_id"
        graph = self._build_graph(sql)
        json_str = json.dumps(graph.to_dict(), ensure_ascii=False)
        restored = json.loads(json_str)
        assert restored["version"] == "1.0"
        assert len(restored["operators"]) > 0

    def test_urn_format(self) -> None:
        graph = self._build_graph("SELECT * FROM ods.orders")
        for ds in graph.datasets:
            assert ds.urn.startswith("urn:li:dataset:(urn:li:dataPlatform:")
            assert "ods" in ds.urn or "default" in ds.urn

    def test_operator_ids_all_unique_in_graph(self) -> None:
        sql = """
        SELECT u.user_id, SUM(o.amount) AS total
        FROM ods.orders o
        JOIN dim.users u ON o.user_id = u.user_id
        WHERE o.status = 'PAID'
        GROUP BY u.user_id
        HAVING SUM(o.amount) > 100
        """
        graph = self._build_graph(sql)
        ids = [op.id for op in graph.operators]
        assert len(ids) == len(set(ids)), f"Duplicate operator IDs: {ids}"


# ================================================================== #
# 12. Corpus file parsing (smoke tests)                                #
# ================================================================== #


@pytest.mark.parametrize("sql_file", sorted(SPARK_CORPUS.glob("*.sql")))
def test_spark_corpus_file_parses(sql_file: Path) -> None:
    """Every Spark corpus file should parse without exception and
    produce at least one operator."""
    sql = sql_file.read_text(encoding="utf-8")
    parser = SqlParser(engine=SqlEngine.SPARK)
    builder = LineageBuilder()
    parsed = parser.parse(sql)
    graph = builder.build(parsed)
    d = graph.to_dict()

    assert d["version"] == "1.0"
    assert d["statement"]["engine"] == "SPARK"
    assert len(d["operators"]) >= 1, f"No operators for {sql_file.name}"

    # JSON must be serializable
    json.dumps(d, ensure_ascii=False)


@pytest.mark.parametrize("sql_file", sorted(OG_CORPUS.glob("*.sql")))
def test_opengauss_corpus_file_parses(sql_file: Path) -> None:
    """Every OpenGauss corpus file should parse without exception and
    produce at least one operator."""
    sql = sql_file.read_text(encoding="utf-8")
    parser = SqlParser(engine=SqlEngine.OPENGAUSS)
    builder = LineageBuilder()
    parsed = parser.parse(sql)
    graph = builder.build(parsed)
    d = graph.to_dict()

    assert d["version"] == "1.0"
    assert d["statement"]["engine"] == "OPENGAUSS"
    assert len(d["operators"]) >= 1, f"No operators for {sql_file.name}"

    json.dumps(d, ensure_ascii=False)


# ================================================================== #
# 13. Macro variable regression tests                                  #
# ================================================================== #


class TestMacroRegression:
    """Ensure macros in various positions are correctly handled."""

    def setup_method(self) -> None:
        self.parser = SqlParser(engine=SqlEngine.SPARK)
        self.builder = LineageBuilder()

    def _run(self, sql: str) -> dict:
        return self.builder.build(self.parser.parse(sql)).to_dict()

    def test_macro_in_where(self) -> None:
        d = self._run("SELECT * FROM ods.orders WHERE dt = {report_date}")
        assert any("{report_date}" in m for m in d["statement"]["macros"])

    def test_macro_in_partition_spec(self) -> None:
        sql = "INSERT OVERWRITE TABLE ads.report PARTITION(dt={dt}) SELECT 1"
        d = self._run(sql)
        assert "{dt}" in d["statement"]["macros"]

    def test_macro_as_table_name(self) -> None:
        sql = "SELECT * FROM {source_db}.{source_table} WHERE x > 1"
        d = self._run(sql)
        macros = d["statement"]["macros"]
        assert "{source_db}" in macros or "{source_table}" in macros

    def test_macro_does_not_break_parsing(self) -> None:
        """A heavily macro-parametrized query should still yield operators."""
        sql = """
        INSERT INTO {target_db}.{target_table} PARTITION (dt={stat_date})
        SELECT {metric_id}, {dim_col_1}, {measure_expr}
        FROM {source_db}.{source_table}
        WHERE dt = {stat_date} AND {filter_condition}
        GROUP BY {dim_col_1}
        """
        d = self._run(sql)
        assert len(d["operators"]) >= 1


# ================================================================== #
# 14. Metadata JSON validation                                         #
# ================================================================== #


class TestMetadataJson:
    def _load(self, name: str) -> dict:
        path = META_DIR / name
        assert path.exists(), f"Metadata file not found: {path}"
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def test_spark_metadata_structure(self) -> None:
        meta = self._load("spark_metadata.json")
        assert meta["engine"] == "SPARK"
        assert len(meta["datasets"]) >= 5

        for ds in meta["datasets"]:
            assert "id" in ds
            assert "urn" in ds
            assert "primary_keys" in ds
            assert isinstance(ds["columns"], list)
            assert len(ds["columns"]) >= 2

    def test_opengauss_metadata_structure(self) -> None:
        meta = self._load("opengauss_metadata.json")
        assert meta["engine"] == "OPENGAUSS"
        assert len(meta["datasets"]) >= 5

    def test_primary_key_columns_marked(self) -> None:
        for fname in ["spark_metadata.json", "opengauss_metadata.json"]:
            meta = self._load(fname)
            for ds in meta["datasets"]:
                pk_cols = [c for c in ds["columns"] if c.get("primary_key")]
                assert len(pk_cols) >= 1, f"Dataset {ds['table']} has no PK column"

    def test_bilingual_column_names(self) -> None:
        """Every column must have both English name and Chinese name."""
        for fname in ["spark_metadata.json", "opengauss_metadata.json"]:
            meta = self._load(fname)
            for ds in meta["datasets"]:
                for col in ds["columns"]:
                    assert "name_en" in col, f"Missing name_en: {col}"
                    assert "name_cn" in col, f"Missing name_cn: {col}"

    def test_urn_format(self) -> None:
        for fname in ["spark_metadata.json", "opengauss_metadata.json"]:
            meta = self._load(fname)
            for ds in meta["datasets"]:
                assert ds["urn"].startswith("urn:li:dataset:(urn:li:dataPlatform:")

    def test_partitioned_tables_have_partition_keys(self) -> None:
        for fname in ["spark_metadata.json", "opengauss_metadata.json"]:
            meta = self._load(fname)
            for ds in meta["datasets"]:
                if ds.get("is_partitioned"):
                    assert len(ds.get("partition_keys", [])) >= 1, (
                        f"{ds['table']} is_partitioned=True but has no partition_keys"
                    )


# ================================================================== #
# 15. Complex lineage scenario                                         #
# ================================================================== #


class TestComplexLineage:
    """End-to-end lineage for a multi-join, multi-CTE, window+agg query."""

    SQL = """
    WITH
    raw_orders AS (
        SELECT order_id, user_id, order_amount, pay_channel, created_at
        FROM ods.orders
        WHERE dt = '2024-01-01' AND order_status = 'PAID'
    ),
    user_summary AS (
        SELECT user_id, SUM(order_amount) AS total_amt, COUNT(*) AS order_cnt
        FROM raw_orders
        GROUP BY user_id
    ),
    ranked AS (
        SELECT user_id, total_amt, order_cnt,
               RANK() OVER (ORDER BY total_amt DESC) AS rnk
        FROM user_summary
    )
    INSERT OVERWRITE TABLE ads.top_users PARTITION (dt='2024-01-01')
    SELECT r.user_id, r.total_amt, r.order_cnt, r.rnk, u.city, u.vip_level, '2024-01-01' AS dt
    FROM ranked r
    JOIN dim.users u ON r.user_id = u.user_id
    WHERE r.rnk <= 100;
    """

    def setup_method(self) -> None:
        self.graph = LineageBuilder().build(
            SqlParser(engine=SqlEngine.SPARK).parse(self.SQL)
        )

    def test_operator_types_present(self) -> None:
        types = {op.type for op in self.graph.operators}
        for expected in [
            OperatorType.SCAN,
            OperatorType.FILTER,
            OperatorType.AGGREGATE,
            OperatorType.WINDOW,
            OperatorType.JOIN,
            OperatorType.PROJECT,
            OperatorType.WRITE,
        ]:
            assert expected in types, f"Missing operator type: {expected}"

    def test_ctes_detected(self) -> None:
        sql_parsed = SqlParser(engine=SqlEngine.SPARK).parse(self.SQL)
        assert "raw_orders" in sql_parsed.ctes
        assert "user_summary" in sql_parsed.ctes
        assert "ranked" in sql_parsed.ctes

    def test_write_is_overwrite(self) -> None:
        write_ops = [op for op in self.graph.operators if op.type == OperatorType.WRITE]
        assert any(op.subtype == OperatorSubtype.OVERWRITE_WRITE for op in write_ops)

    def test_graph_json_valid(self) -> None:
        d = self.graph.to_dict()
        serialized = json.dumps(d, ensure_ascii=False)
        restored = json.loads(serialized)
        assert restored["version"] == "1.0"
        assert len(restored["operators"]) >= 5
