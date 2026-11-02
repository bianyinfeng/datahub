"""
Unit tests for the ANTLR4-based SQL visitor (antlr4_visitor.py).

These tests verify that the real ANTLR4 parser correctly extracts
lineage-relevant information from SQL without regex heuristics.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from datahub.sql_parsing.antlr4.antlr4_visitor import parse_sql
from datahub.sql_parsing.antlr4.lineage_builder import LineageBuilder
from datahub.sql_parsing.antlr4.models import SqlEngine

_BUILDER = LineageBuilder()
_CORPUS = Path(__file__).parent.parent / "corpus"


# ── helpers ──────────────────────────────────────────────────────────────────

def _tables(sources):
    return {t for _, t, _ in sources}


# ── statement type ────────────────────────────────────────────────────────────

class TestStatementType:
    def test_select(self):
        stmt = parse_sql("SELECT a FROM t", SqlEngine.SPARK)
        assert stmt.statement_type == "SELECT"

    def test_cte_select(self):
        stmt = parse_sql("WITH c AS (SELECT 1) SELECT * FROM c", SqlEngine.SPARK)
        assert stmt.statement_type == "SELECT"

    def test_insert_into(self):
        stmt = parse_sql("INSERT INTO dwd.orders SELECT * FROM ods.raw", SqlEngine.SPARK)
        assert stmt.statement_type == "INSERT"

    def test_insert_overwrite(self):
        stmt = parse_sql("INSERT OVERWRITE dws.sales SELECT * FROM dwd.orders", SqlEngine.SPARK)
        assert stmt.statement_type == "INSERT_OVERWRITE"

    def test_merge_spark(self):
        sql = ("MERGE INTO tgt USING src ON tgt.id=src.id "
               "WHEN MATCHED THEN UPDATE SET x=src.x")
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert stmt.statement_type == "MERGE"

    def test_merge_opengauss(self):
        sql = ("MERGE INTO orders t USING staging s ON t.id=s.id "
               "WHEN MATCHED THEN UPDATE SET status=s.status "
               "WHEN NOT MATCHED THEN INSERT VALUES(s.id, s.status)")
        stmt = parse_sql(sql, SqlEngine.OPENGAUSS)
        assert stmt.statement_type == "MERGE"

    def test_ctas(self):
        stmt = parse_sql("CREATE TABLE t USING delta AS SELECT * FROM s", SqlEngine.SPARK)
        assert stmt.statement_type == "CTAS"

    def test_create_view(self):
        stmt = parse_sql("CREATE OR REPLACE VIEW v AS SELECT * FROM t", SqlEngine.SPARK)
        assert stmt.statement_type == "CREATE_VIEW"

    def test_create_mat_view(self):
        stmt = parse_sql("CREATE MATERIALIZED VIEW mv AS SELECT * FROM t", SqlEngine.OPENGAUSS)
        assert stmt.statement_type == "CREATE_MATERIALIZED_VIEW"


# ── macro variables ───────────────────────────────────────────────────────────

class TestMacroExtraction:
    def test_single_macro(self):
        stmt = parse_sql("SELECT * FROM t WHERE dt = {report_date}", SqlEngine.SPARK)
        assert "report_date" in stmt.macros

    def test_multiple_macros(self):
        stmt = parse_sql(
            "INSERT INTO {target} SELECT {col} FROM {src} WHERE {flt}",
            SqlEngine.SPARK,
        )
        for m in ("target", "col", "src", "flt"):
            assert m in stmt.macros

    def test_macro_in_table_name(self):
        stmt = parse_sql("SELECT * FROM {source_schema}.events", SqlEngine.SPARK)
        assert "source_schema" in stmt.macros

    def test_no_macros(self):
        stmt = parse_sql("SELECT id FROM users", SqlEngine.SPARK)
        assert stmt.macros == []


# ── table references ──────────────────────────────────────────────────────────

class TestTableExtraction:
    def test_simple_from(self):
        stmt = parse_sql("SELECT a FROM ods.orders", SqlEngine.SPARK)
        tables = _tables(stmt.source_tables)
        assert "orders" in tables

    def test_schema_qualified(self):
        stmt = parse_sql("SELECT a FROM dw.schema.fact_sales", SqlEngine.SPARK)
        assert any("fact_sales" in t for _, t, _ in stmt.source_tables)

    def test_cte_excluded_from_sources(self):
        sql = "WITH cte AS (SELECT id FROM raw) SELECT * FROM cte JOIN other ON cte.id=other.id"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        tables = _tables(stmt.source_tables)
        assert "cte" not in tables
        assert "raw" in tables
        assert "other" in tables

    def test_insert_target(self):
        stmt = parse_sql("INSERT INTO dws.sales SELECT * FROM dwd.orders", SqlEngine.SPARK)
        assert any("sales" in t for _, t in stmt.target_tables)

    def test_ctas_target(self):
        stmt = parse_sql("CREATE TABLE dws.result AS SELECT * FROM ods.raw", SqlEngine.SPARK)
        assert any("result" in t for _, t in stmt.target_tables)


# ── JOIN extraction ───────────────────────────────────────────────────────────

class TestJoinExtraction:
    def test_inner_join(self):
        sql = "SELECT * FROM a JOIN b ON a.id=b.id"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert any(j["type"] == "INNER" for j in stmt.joins)

    def test_left_join(self):
        sql = "SELECT * FROM a LEFT JOIN b ON a.id=b.id"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert any(j["type"] == "LEFT" for j in stmt.joins)

    def test_full_join(self):
        sql = "SELECT * FROM a FULL OUTER JOIN b ON a.id=b.id"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert any(j["type"] == "FULL" for j in stmt.joins)

    def test_cross_join(self):
        sql = "SELECT * FROM a CROSS JOIN b"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert any(j["type"] == "CROSS" for j in stmt.joins)


# ── filter / group by / window ────────────────────────────────────────────────

class TestAnalyticsExtraction:
    def test_where_filter(self):
        stmt = parse_sql("SELECT * FROM t WHERE id > 0", SqlEngine.SPARK)
        assert any(f["type"] == "WHERE" for f in stmt.filters)

    def test_having_filter(self):
        stmt = parse_sql("SELECT a, COUNT(*) FROM t GROUP BY a HAVING COUNT(*) > 1", SqlEngine.SPARK)
        assert any(f["type"] == "HAVING" for f in stmt.filters)

    def test_group_by(self):
        stmt = parse_sql("SELECT a, SUM(b) FROM t GROUP BY a", SqlEngine.SPARK)
        assert len(stmt.group_by) > 0

    def test_window_function(self):
        sql = "SELECT id, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC) AS rn FROM emp"
        stmt = parse_sql(sql, SqlEngine.SPARK)
        assert len(stmt.windows) > 0

    def test_union_all(self):
        stmt = parse_sql("SELECT a FROM t1 UNION ALL SELECT a FROM t2", SqlEngine.SPARK)
        assert any(op == "UNION_ALL" for op, _ in stmt.set_ops)

    def test_recursive_cte(self):
        sql = "WITH RECURSIVE r(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM r WHERE n<5) SELECT * FROM r"
        stmt = parse_sql(sql, SqlEngine.OPENGAUSS)
        assert stmt.statement_type == "SELECT"
        assert "r" in stmt.ctes


# ── OpenGauss specifics ───────────────────────────────────────────────────────

class TestOpenGaussSpecifics:
    def test_returning_clause(self):
        stmt = parse_sql(
            "INSERT INTO orders SELECT * FROM staging RETURNING id, created_at",
            SqlEngine.OPENGAUSS,
        )
        assert len(stmt.returning) > 0

    def test_jsonb_query(self):
        stmt = parse_sql(
            "SELECT data->'key' FROM events WHERE data->>'status' = 'active'",
            SqlEngine.OPENGAUSS,
        )
        assert stmt.statement_type == "SELECT"
        assert _tables(stmt.source_tables) == {"events"}

    def test_full_text_search(self):
        stmt = parse_sql(
            "SELECT * FROM docs WHERE to_tsvector('english', content) @@ plainto_tsquery({q})",
            SqlEngine.OPENGAUSS,
        )
        assert "q" in stmt.macros

    def test_merge_extract_target(self):
        sql = ("MERGE INTO dws.orders t USING staging s ON t.id=s.id "
               "WHEN MATCHED THEN UPDATE SET status=s.status "
               "WHEN NOT MATCHED THEN INSERT VALUES(s.id, s.status)")
        stmt = parse_sql(sql, SqlEngine.OPENGAUSS)
        assert any("orders" in t for _, t in stmt.target_tables)


# ── full lineage graph ────────────────────────────────────────────────────────

class TestLineageGraph:
    def test_simple_select_has_scan_and_project(self):
        stmt = parse_sql("SELECT a, b FROM ods.orders WHERE dt = '2024-01-01'", SqlEngine.SPARK)
        graph = _BUILDER.build(stmt)
        d = graph.to_dict()
        op_types = {op["type"] for op in d["operators"]}
        assert "SCAN" in op_types
        assert "FILTER" in op_types

    def test_insert_has_write(self):
        stmt = parse_sql("INSERT INTO dws.fact SELECT * FROM dwd.dim", SqlEngine.SPARK)
        graph = _BUILDER.build(stmt)
        d = graph.to_dict()
        assert any(op["type"] == "WRITE" for op in d["operators"])

    def test_no_duplicate_operator_ids(self):
        sql = """
        WITH a AS (SELECT id, SUM(amt) AS tot FROM raw GROUP BY id),
             b AS (SELECT * FROM a WHERE tot > 0)
        SELECT * FROM b LEFT JOIN extra e ON b.id = e.id
        """
        stmt = parse_sql(sql, SqlEngine.SPARK)
        graph = _BUILDER.build(stmt)
        d = graph.to_dict()
        ids = [op["id"] for op in d["operators"]]
        assert len(ids) == len(set(ids)), "Duplicate operator IDs"

    def test_json_roundtrip(self):
        import json
        stmt = parse_sql("SELECT a, b FROM t1 JOIN t2 ON t1.id=t2.id WHERE a > 0", SqlEngine.SPARK)
        graph = _BUILDER.build(stmt)
        d = graph.to_dict()
        serialized = json.dumps(d, default=str)
        deserialized = json.loads(serialized)
        assert deserialized["operators"] == d["operators"]


# ── corpus smoke tests ────────────────────────────────────────────────────────

class TestCorpusSmoke:
    def _run_corpus(self, subdir: str, engine: SqlEngine) -> None:
        corpus_dir = _CORPUS / subdir
        assert corpus_dir.exists(), f"Corpus dir missing: {corpus_dir}"
        files = sorted(corpus_dir.glob("*.sql"))
        assert len(files) >= 50, f"Expected >=50 corpus files, found {len(files)}"
        errors = []
        for f in files:
            sql = f.read_text()
            try:
                stmt = parse_sql(sql, engine)
                graph = _BUILDER.build(stmt)
                d = graph.to_dict()
                assert len(d["operators"]) > 0, f"{f.name}: empty operator list"
            except Exception as e:
                errors.append(f"{f.name}: {e}")
        assert not errors, f"{len(errors)} corpus files failed:\n" + "\n".join(errors[:5])

    def test_spark_corpus(self):
        self._run_corpus("spark", SqlEngine.SPARK)

    def test_opengauss_corpus(self):
        self._run_corpus("opengauss", SqlEngine.OPENGAUSS)
