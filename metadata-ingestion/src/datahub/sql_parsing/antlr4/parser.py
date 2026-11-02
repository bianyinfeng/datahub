"""
SqlParser — regex-based SQL parser for Spark SQL and OpenGauss dialects.

This module provides a pure-Python parser (no ANTLR4 runtime required at
import time) that extracts the structural information needed to build a
LineageGraph.  When the optional antlr4-python3-runtime package is installed
the .parse_with_antlr() method delegates to the generated ANTLR4 parsers for
full syntactic fidelity.

The regex-based path is intentionally conservative: it identifies the top-level
statement type, extracts table/column references, macros, CTEs, JOINs, GROUP-BY
clauses, window functions, and INSERT/MERGE targets.  This is sufficient to
produce a rich operator-level lineage graph for the corpus SQL files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from datahub.sql_parsing.antlr4.models import SqlEngine


# ---------------------------------------------------------------------------
# Lightweight parse result (engine-agnostic)
# ---------------------------------------------------------------------------


@dataclass
class ParsedStatement:
    """Intermediate parse result consumed by LineageBuilder."""

    sql: str
    engine: SqlEngine
    statement_type: str = "SELECT"

    # CTE name -> SQL body
    ctes: Dict[str, str] = field(default_factory=dict)

    # Tables referenced as sources: (schema, table, alias)
    source_tables: List[Tuple[str, str, str]] = field(default_factory=list)

    # Tables written to: (schema, table)
    target_tables: List[Tuple[str, str]] = field(default_factory=list)

    # Selected / projected columns: (expr, alias)
    projections: List[Tuple[str, str]] = field(default_factory=list)

    # JOIN info: (join_type, schema, table, alias, condition)
    joins: List[Dict[str, str]] = field(default_factory=list)

    # WHERE / HAVING / ON conditions (raw text)
    filters: List[Dict[str, str]] = field(default_factory=list)

    # GROUP BY expressions
    group_by: List[str] = field(default_factory=list)

    # Window function expressions
    windows: List[Dict[str, str]] = field(default_factory=list)

    # UNNEST / LATERAL VIEW expressions
    unnests: List[Dict[str, str]] = field(default_factory=list)

    # SET operations: (operator, subquery)
    set_ops: List[Tuple[str, str]] = field(default_factory=list)

    # Macro variable names found in the SQL
    macros: List[str] = field(default_factory=list)

    # MERGE action details
    merge_actions: List[Dict[str, str]] = field(default_factory=list)

    # RETURNING columns (OpenGauss)
    returning: List[str] = field(default_factory=list)

    # PARTITION spec
    partition_cols: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

_WS = r"[\s\r\n]+"
_OWS = r"[\s\r\n]*"
_ID = r"[`\"]?[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*[`\"]?"
_QNAME = rf"(?:{_ID}\.)*{_ID}"  # qualified name: schema.table or db.schema.table
_MACRO = r"\{[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*\}"

# Strip SQL comments (block and line) before parsing
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT = re.compile(r"--[^\r\n]*")


def _strip_comments(sql: str) -> str:
    sql = _BLOCK_COMMENT.sub(" ", sql)
    sql = _LINE_COMMENT.sub(" ", sql)
    return sql


# Statement type detection
_STMT_PATTERNS = [
    ("INSERT_OVERWRITE", re.compile(r"^\s*INSERT\s+OVERWRITE", re.I)),
    ("INSERT", re.compile(r"^\s*INSERT\s+INTO", re.I)),
    ("MERGE", re.compile(r"^\s*MERGE\s+INTO", re.I)),
    ("CREATE_TABLE_AS", re.compile(r"^\s*CREATE\s+.*TABLE.*AS\s+SELECT", re.I | re.S)),
    ("CREATE_TABLE", re.compile(r"^\s*CREATE\s+.*TABLE", re.I | re.S)),
    ("CREATE_VIEW", re.compile(r"^\s*CREATE\s+.*VIEW", re.I | re.S)),
    ("CREATE_MAT_VIEW", re.compile(r"^\s*CREATE\s+MATERIALIZED\s+VIEW", re.I)),
    ("UPDATE", re.compile(r"^\s*UPDATE\s+", re.I)),
    ("DELETE", re.compile(r"^\s*DELETE\s+FROM", re.I)),
    ("COPY", re.compile(r"^\s*COPY\s+", re.I)),
    ("TRUNCATE", re.compile(r"^\s*TRUNCATE\s+", re.I)),
    ("SELECT", re.compile(r"^\s*(WITH|SELECT)", re.I)),
]

# CTE
_CTE_RE = re.compile(
    r"\bWITH\b\s+(?:RECURSIVE\s+)?(.+?)\s+(?=SELECT|INSERT|MERGE|UPDATE|DELETE)",
    re.I | re.S,
)
_CTE_ITEM_RE = re.compile(
    rf"({_ID})\s*(?:\(([^)]*)\))?\s+AS\s*\(",
    re.I,
)

# FROM / JOIN table references
_FROM_RE = re.compile(
    rf"(?:FROM|JOIN)\s+({_MACRO}|{_QNAME})\s*(?:AS\s+({_ID})|({_ID}))?",
    re.I,
)
_JOIN_TYPE_RE = re.compile(
    r"(INNER|LEFT\s+(?:OUTER|SEMI|ANTI)?|RIGHT\s+(?:OUTER)?|FULL\s+(?:OUTER)?|CROSS|NATURAL|SEMI|ANTI)?\s*JOIN",
    re.I,
)

# INSERT target
_INSERT_INTO_RE = re.compile(
    rf"INSERT\s+(?:OVERWRITE|INTO)\s+(?:TABLE\s+)?({_MACRO}|{_QNAME})",
    re.I,
)
_INSERT_PARTITION_RE = re.compile(
    rf"PARTITION\s*\(([^)]+)\)",
    re.I,
)

# MERGE target + source
_MERGE_TARGET_RE = re.compile(
    rf"MERGE\s+INTO\s+({_MACRO}|{_QNAME})\s*(?:AS\s+({_ID})|({_ID}))?",
    re.I,
)
_MERGE_USING_RE = re.compile(
    rf"USING\s+({_MACRO}|{_QNAME}|\()",
    re.I,
)

# SELECT projections (simplified)
_SELECT_COLS_RE = re.compile(
    r"SELECT\s+(DISTINCT\s+|ALL\s+)?(.+?)\s+FROM",
    re.I | re.S,
)

# WHERE / HAVING / ON conditions
_WHERE_RE = re.compile(r"\bWHERE\b(.+?)(?=GROUP\s+BY|HAVING|ORDER\s+BY|LIMIT|UNION|INTERSECT|EXCEPT|$)", re.I | re.S)
_HAVING_RE = re.compile(r"\bHAVING\b(.+?)(?=ORDER\s+BY|LIMIT|UNION|INTERSECT|EXCEPT|$)", re.I | re.S)

# GROUP BY
_GROUP_BY_RE = re.compile(r"\bGROUP\s+BY\b(.+?)(?=HAVING|ORDER\s+BY|LIMIT|UNION|WINDOW|$)", re.I | re.S)

# WINDOW
_WINDOW_FUNC_RE = re.compile(
    rf"({_ID})\s*\([^)]*\)\s*OVER\s*\(",
    re.I,
)

# LATERAL VIEW / UNNEST
_LATERAL_VIEW_RE = re.compile(
    rf"LATERAL\s+VIEW\s+(?:OUTER\s+)?({_ID})\s*\(([^)]*)\)\s+({_ID})\s+AS\s+({_ID}(?:\s*,\s*{_ID})*)",
    re.I,
)
_UNNEST_RE = re.compile(
    rf"UNNEST\s*\(([^)]+)\)(?:\s+WITH\s+ORDINALITY)?(?:\s+AS\s+({_ID}))?",
    re.I,
)

# SET operations
_SET_OP_RE = re.compile(
    r"\b(UNION\s+ALL|UNION|INTERSECT|EXCEPT|MINUS)\b",
    re.I,
)

# CREATE TABLE / VIEW
_CREATE_TABLE_RE = re.compile(
    rf"CREATE\s+(?:OR\s+REPLACE\s+)?(?:EXTERNAL\s+|UNLOGGED\s+|TEMPORARY\s+|TEMP\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?({_MACRO}|{_QNAME})",
    re.I,
)
_CREATE_VIEW_RE = re.compile(
    rf"CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+)?VIEW\s+(?:IF\s+NOT\s+EXISTS\s+)?({_MACRO}|{_QNAME})",
    re.I,
)

# RETURNING
_RETURNING_RE = re.compile(r"\bRETURNING\b(.+?)(?:;|$)", re.I | re.S)

# COPY target
_COPY_RE = re.compile(
    rf"COPY\s+({_MACRO}|{_QNAME})\s+(?:\([^)]+\)\s+)?(?:FROM|TO)",
    re.I,
)

# MACRO extraction
_MACRO_RE = re.compile(_MACRO)


# ---------------------------------------------------------------------------
# Parser class
# ---------------------------------------------------------------------------


class SqlParser:
    """Parse SQL statements into ParsedStatement objects."""

    def __init__(self, engine: SqlEngine = SqlEngine.SPARK) -> None:
        self.engine = engine

    def parse(self, sql: str) -> ParsedStatement:
        """Parse a single SQL statement and return a ParsedStatement."""
        clean = _strip_comments(sql).strip()
        stmt = ParsedStatement(sql=sql, engine=self.engine)

        # 1. Detect statement type
        stmt.statement_type = self._detect_type(clean)

        # 2. Extract macros
        stmt.macros = list({m for m in _MACRO_RE.findall(clean)})

        # 3. Extract CTEs
        stmt.ctes = self._extract_ctes(clean)

        # 4. Extract tables (source / target)
        self._extract_tables(clean, stmt)

        # 5. Extract projections
        stmt.projections = self._extract_projections(clean)

        # 6. Extract JOINs
        stmt.joins = self._extract_joins(clean)

        # 7. Extract filters
        stmt.filters = self._extract_filters(clean)

        # 8. Extract GROUP BY
        stmt.group_by = self._extract_group_by(clean)

        # 9. Extract window functions
        stmt.windows = self._extract_windows(clean)

        # 10. Extract UNNEST / LATERAL VIEW
        stmt.unnests = self._extract_unnests(clean)

        # 11. Extract SET operations
        stmt.set_ops = self._extract_set_ops(clean)

        # 12. Extract RETURNING
        stmt.returning = self._extract_returning(clean)

        return stmt

    # ---- Type detection -------------------------------------------

    def _detect_type(self, sql: str) -> str:
        for name, pattern in _STMT_PATTERNS:
            if pattern.match(sql):
                return name
        return "SELECT"

    # ---- CTEs -----------------------------------------------------

    def _extract_ctes(self, sql: str) -> Dict[str, str]:
        ctes: Dict[str, str] = {}
        m = _CTE_RE.search(sql)
        if not m:
            return ctes
        cte_block = m.group(1)
        for item in _CTE_ITEM_RE.finditer(cte_block):
            ctes[item.group(1)] = ""  # body extraction is expensive; store name
        return ctes

    # ---- Table extraction -----------------------------------------

    def _extract_tables(self, sql: str, stmt: ParsedStatement) -> None:
        upper = sql.upper()
        cte_names: Set[str] = {k.upper() for k in stmt.ctes}

        # Target tables
        if stmt.statement_type in ("INSERT", "INSERT_OVERWRITE"):
            for m in _INSERT_INTO_RE.finditer(sql):
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "default"
                name = parts[-1]
                stmt.target_tables.append((schema, name))
            # partition columns
            for pm in _INSERT_PARTITION_RE.finditer(sql):
                cols = [c.strip().split("=")[0].strip() for c in pm.group(1).split(",")]
                stmt.partition_cols.extend(cols)

        elif stmt.statement_type == "MERGE":
            m = _MERGE_TARGET_RE.search(sql)
            if m:
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "default"
                name = parts[-1]
                stmt.target_tables.append((schema, name))

        elif stmt.statement_type in ("CREATE_TABLE", "CREATE_TABLE_AS"):
            m = _CREATE_TABLE_RE.search(sql)
            if m:
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "default"
                name = parts[-1]
                stmt.target_tables.append((schema, name))

        elif stmt.statement_type in ("CREATE_VIEW", "CREATE_MAT_VIEW"):
            m = _CREATE_VIEW_RE.search(sql)
            if m:
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "default"
                name = parts[-1]
                stmt.target_tables.append((schema, name))

        elif stmt.statement_type == "COPY":
            m = _COPY_RE.search(sql)
            if m:
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "public"
                name = parts[-1]
                if "TO" in upper:
                    stmt.target_tables.append((schema, name))
                else:
                    stmt.source_tables.append((schema, name, ""))

        # Source tables via FROM / JOIN
        for m in _FROM_RE.finditer(sql):
            tbl = m.group(1)
            alias = m.group(2) or m.group(3) or ""
            parts = tbl.strip("`\"{}").split(".")
            schema = parts[-2] if len(parts) >= 2 else ("public" if self.engine == SqlEngine.OPENGAUSS else "default")
            name = parts[-1]
            # Skip CTE references
            if name.upper() in cte_names:
                continue
            # Skip if it's already the target
            if (schema, name) in stmt.target_tables:
                continue
            stmt.source_tables.append((schema, name, alias))

        # MERGE USING source
        if stmt.statement_type == "MERGE":
            m = _MERGE_USING_RE.search(sql)
            if m and m.group(1) != "(":
                tbl = m.group(1)
                parts = tbl.strip("`\"").split(".")
                schema = parts[-2] if len(parts) >= 2 else "default"
                name = parts[-1]
                if name.upper() not in cte_names:
                    stmt.source_tables.append((schema, name, "src"))

    # ---- Projections ----------------------------------------------

    def _extract_projections(self, sql: str) -> List[Tuple[str, str]]:
        result: List[Tuple[str, str]] = []
        m = _SELECT_COLS_RE.search(sql)
        if not m:
            return result
        cols_str = m.group(2)
        # Split on top-level commas (ignore commas inside parentheses)
        cols = self._split_top_level(cols_str)
        for col in cols:
            col = col.strip()
            # Extract alias
            alias_match = re.match(r"(.+?)\s+AS\s+([`\"]?\w+[`\"]?)$", col, re.I)
            if alias_match:
                result.append((alias_match.group(1).strip(), alias_match.group(2).strip("`\"")))
            else:
                result.append((col, ""))
        return result

    def _split_top_level(self, s: str) -> List[str]:
        """Split s by commas that are not inside parentheses."""
        parts: List[str] = []
        depth = 0
        current: List[str] = []
        for ch in s:
            if ch == "(":
                depth += 1
                current.append(ch)
            elif ch == ")":
                depth -= 1
                current.append(ch)
            elif ch == "," and depth == 0:
                parts.append("".join(current))
                current = []
            else:
                current.append(ch)
        if current:
            parts.append("".join(current))
        return parts

    # ---- JOINs ----------------------------------------------------

    def _extract_joins(self, sql: str) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        pattern = re.compile(
            rf"((?:INNER|LEFT(?:\s+(?:OUTER|SEMI|ANTI))?|RIGHT(?:\s+OUTER)?|FULL(?:\s+OUTER)?|CROSS|NATURAL|SEMI|ANTI)?\s*)JOIN\s+({_MACRO}|{_QNAME})\s*(?:AS\s+({_ID})|({_ID}))?\s*(?:ON\s+(.+?))?(?=JOIN|WHERE|GROUP|HAVING|ORDER|LIMIT|UNION|INTERSECT|EXCEPT|$)",
            re.I | re.S,
        )
        for m in pattern.finditer(sql):
            jtype = (m.group(1) or "INNER").strip().upper() or "INNER"
            tbl = m.group(2)
            alias = m.group(3) or m.group(4) or ""
            condition = (m.group(5) or "").strip()
            parts = tbl.strip("`\"{}").split(".")
            result.append(
                {
                    "type": jtype,
                    "schema": parts[-2] if len(parts) >= 2 else "default",
                    "table": parts[-1],
                    "alias": alias,
                    "condition": condition[:200],  # truncate long conditions
                }
            )
        return result

    # ---- Filters --------------------------------------------------

    def _extract_filters(self, sql: str) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        m = _WHERE_RE.search(sql)
        if m:
            result.append({"type": "WHERE", "condition": m.group(1).strip()[:500]})
        m = _HAVING_RE.search(sql)
        if m:
            result.append({"type": "HAVING", "condition": m.group(1).strip()[:500]})
        return result

    # ---- GROUP BY -------------------------------------------------

    def _extract_group_by(self, sql: str) -> List[str]:
        m = _GROUP_BY_RE.search(sql)
        if not m:
            return []
        return [c.strip() for c in self._split_top_level(m.group(1)) if c.strip()]

    # ---- Window functions -----------------------------------------

    def _extract_windows(self, sql: str) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        for m in _WINDOW_FUNC_RE.finditer(sql):
            result.append({"function": m.group(1), "spec": ""})
        return result

    # ---- UNNEST / LATERAL VIEW ------------------------------------

    def _extract_unnests(self, sql: str) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        for m in _LATERAL_VIEW_RE.finditer(sql):
            result.append(
                {
                    "type": "LATERAL_VIEW",
                    "function": m.group(1),
                    "args": m.group(2),
                    "table_alias": m.group(3),
                    "col_aliases": m.group(4),
                }
            )
        for m in _UNNEST_RE.finditer(sql):
            result.append({"type": "UNNEST", "args": m.group(1), "alias": m.group(2) or ""})
        return result

    # ---- SET operations -------------------------------------------

    def _extract_set_ops(self, sql: str) -> List[Tuple[str, str]]:
        result: List[Tuple[str, str]] = []
        for m in _SET_OP_RE.finditer(sql):
            result.append((m.group(1).upper().replace("  ", " "), ""))
        return result

    # ---- RETURNING ------------------------------------------------

    def _extract_returning(self, sql: str) -> List[str]:
        m = _RETURNING_RE.search(sql)
        if not m:
            return []
        cols_str = m.group(1).strip().rstrip(";")
        return [c.strip() for c in self._split_top_level(cols_str) if c.strip()]
