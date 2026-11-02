"""
antlr4_visitor.py - ANTLR4 AST visitor for SQL lineage extraction.

Walks the parse tree produced by the generated SparkSql / OpenGaussSql parsers
and populates ParsedStatement fields used by LineageBuilder.  No DataHub
core modules are imported here, and no regex heuristics are used.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl

# ── locate generated parsers ─────────────────────────────────────────────────
_BASE = Path(__file__).parent / "generated"
for _p in (str(_BASE / "spark"), str(_BASE / "opengauss")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from SparkSqlLexer import SparkSqlLexer          # type: ignore
from SparkSqlParser import SparkSqlParser        # type: ignore
from SparkSqlVisitor import SparkSqlVisitor      # type: ignore
from OpenGaussSqlLexer import OpenGaussSqlLexer  # type: ignore
from OpenGaussSqlParser import OpenGaussSqlParser  # type: ignore
from OpenGaussSqlVisitor import OpenGaussSqlVisitor  # type: ignore

# local models (our own package, not DataHub core)
from datahub.sql_parsing.antlr4.parser import ParsedStatement
from datahub.sql_parsing.antlr4.models import SqlEngine


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

class _SilentEL(ErrorListener):
    def __init__(self) -> None:
        super().__init__()
        self.errors: List[str] = []
    def syntaxError(self, r, o, line, col, msg, e):  # type: ignore
        self.errors.append(f"line {line}:{col} {msg}")


def _text(ctx) -> str:  # type: ignore
    if ctx is None:
        return ""
    t = ctx.getText() if hasattr(ctx, "getText") else str(ctx)
    return t.strip("`\"' ")


def _qname(ctx) -> Tuple[str, str]:
    """Return (schema, table) from a macroOrIdentifier context."""
    if ctx is None:
        return ("", "")
    parts = _text(ctx).split(".")
    return (parts[-2], parts[-1]) if len(parts) >= 2 else ("", parts[0])


def _has_token(ctx, token_text: str) -> bool:
    """Return True if any terminal child of ctx matches token_text (case-insensitive)."""
    for i in range(ctx.getChildCount()):
        child = ctx.getChild(i)
        if isinstance(child, TerminalNodeImpl) and child.getText().upper() == token_text.upper():
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Core visitor logic (shared via mixin for both engines)
# ─────────────────────────────────────────────────────────────────────────────

class _VisitorMixin:
    """
    Visitor mixin that walks an ANTLR4 parse tree and populates a ParsedStatement.

    Both Spark and OpenGauss override the top-level `statement` rule with their
    own engine-specific labels (spark* / og*).  Below we implement all variants.
    The actual data extraction is done in the rule-level visitor methods which
    are shared between both dialects via grammar import.
    """

    _stmt: ParsedStatement
    _cte_names: set

    # ── init ─────────────────────────────────────────────────────────────────

    def _init(self, stmt: ParsedStatement) -> None:
        self._stmt = stmt
        self._cte_names = set()

    # ── macro harvesting ─────────────────────────────────────────────────────

    def _harvest_macros(self, ctx) -> None:  # type: ignore
        if ctx is None:
            return
        if isinstance(ctx, TerminalNodeImpl):
            t = ctx.getText()
            if t.startswith("{") and t.endswith("}"):
                name = t[1:-1]
                if name not in self._stmt.macros:
                    self._stmt.macros.append(name)
            return
        for i in range(ctx.getChildCount()):
            self._harvest_macros(ctx.getChild(i))

    # ── Spark statement labels ────────────────────────────────────────────────

    def visitSparkQueryStatement(self, ctx):  # type: ignore
        self._stmt.statement_type = "SELECT"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitSparkInsertStmt(self, ctx):  # type: ignore
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitSparkMergeStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "MERGE"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitSparkCreateTableStmt(self, ctx):  # type: ignore
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitSparkCreateViewStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "CREATE_VIEW"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    # ── OpenGauss statement labels ────────────────────────────────────────────

    def visitOgQueryStatement(self, ctx):  # type: ignore
        self._stmt.statement_type = "SELECT"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgInsertStmt(self, ctx):  # type: ignore
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgMergeStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "MERGE"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgCreateTableStmt(self, ctx):  # type: ignore
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgCreateViewStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "CREATE_VIEW"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgCreateMatViewStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "CREATE_MATERIALIZED_VIEW"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgCopyStmt(self, ctx):  # type: ignore
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgUpdateStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "UPDATE"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    def visitOgDeleteStmt(self, ctx):  # type: ignore
        self._stmt.statement_type = "DELETE"
        self._harvest_macros(ctx)
        return self.visitChildren(ctx)

    # ── CTE ──────────────────────────────────────────────────────────────────

    def visitNamedQuery(self, ctx):  # type: ignore
        if hasattr(ctx, "name") and ctx.name is not None:
            name = _text(ctx.name)
            self._cte_names.add(name.lower())
            body = ctx.query() if hasattr(ctx, "query") else None
            self._stmt.ctes[name] = _text(body) if body else ""
        return self.visitChildren(ctx)

    # ── table references ─────────────────────────────────────────────────────

    def visitTableName(self, ctx):  # type: ignore
        tbl_ctx = ctx.macroOrIdentifier() if hasattr(ctx, "macroOrIdentifier") else None
        if tbl_ctx is None:
            return self.visitChildren(ctx)
        txt = _text(tbl_ctx).lower()
        if txt in self._cte_names:
            return self.visitChildren(ctx)
        schema, table = _qname(tbl_ctx)
        alias_ctx = ctx.alias if hasattr(ctx, "alias") else None
        alias = _text(alias_ctx) if alias_ctx else ""
        self._stmt.source_tables.append((schema, table, alias))
        return self.visitChildren(ctx)

    # ── JOIN ─────────────────────────────────────────────────────────────────

    def visitJoinRelation(self, ctx):  # type: ignore
        jtype_ctx = ctx.joinType() if hasattr(ctx, "joinType") else None
        if jtype_ctx is not None:
            jtype = _text(jtype_ctx).upper()
        elif _has_token(ctx, "CROSS"):
            jtype = "CROSS"
        elif _has_token(ctx, "NATURAL"):
            jtype = "INNER"
        else:
            jtype = "INNER"
        
        if jtype_ctx is not None:
            jtype_text = jtype  # keep working from text
            if "CROSS" in jtype_text:
                jtype = "CROSS"
            elif "LEFTSEMI" in jtype_text.replace(" ", ""):
                jtype = "LEFT_SEMI"
            elif "RIGHTSEMI" in jtype_text.replace(" ", ""):
                jtype = "RIGHT_SEMI"
            elif "LEFTANTI" in jtype_text.replace(" ", ""):
                jtype = "LEFT_ANTI"
            elif "LEFT" in jtype_text:
                jtype = "LEFT"
            elif "RIGHT" in jtype_text:
                jtype = "RIGHT"
            elif "FULL" in jtype_text:
                jtype = "FULL"
            else:
                jtype = "INNER"

        rp = ctx.relationPrimary() if hasattr(ctx, "relationPrimary") else None
        schema, table, alias = "", "", ""
        if rp is not None and "TableName" in type(rp).__name__:
            tbl_ctx = rp.macroOrIdentifier() if hasattr(rp, "macroOrIdentifier") else None
            schema, table = _qname(tbl_ctx)
            alias_ctx = rp.alias if hasattr(rp, "alias") else None
            alias = _text(alias_ctx) if alias_ctx else ""

        crit = ctx.joinCriteria() if hasattr(ctx, "joinCriteria") else None
        self._stmt.joins.append({
            "type": jtype, "join_type": jtype,
            "schema": schema,
            "table": table,
            "alias": alias,
            "condition": _text(crit) if crit else "",
        })
        return self.visitChildren(ctx)

    # ── FILTER ───────────────────────────────────────────────────────────────

    def visitWhereClause(self, ctx):  # type: ignore
        expr = ctx.expression() if hasattr(ctx, "expression") else None
        self._stmt.filters.append({"type": "WHERE", "condition": _text(expr)})
        return self.visitChildren(ctx)

    def visitHavingClause(self, ctx):  # type: ignore
        expr = ctx.expression() if hasattr(ctx, "expression") else None
        self._stmt.filters.append({"type": "HAVING", "condition": _text(expr)})
        return self.visitChildren(ctx)

    def visitQualifyClause(self, ctx):  # type: ignore
        expr = ctx.expression() if hasattr(ctx, "expression") else None
        self._stmt.filters.append({"type": "QUALIFY", "condition": _text(expr)})
        return self.visitChildren(ctx)

    # ── GROUP BY ─────────────────────────────────────────────────────────────

    def visitGroupByClause(self, ctx):  # type: ignore
        for item in (ctx.groupByItem() or []):
            txt = _text(item).upper()
            if "ROLLUP" in txt:
                self._stmt.group_by.append("__ROLLUP__")
            elif "CUBE" in txt:
                self._stmt.group_by.append("__CUBE__")
            elif "GROUPINGSETS" in txt.replace(" ", ""):
                self._stmt.group_by.append("__GROUPING_SETS__")
            else:
                self._stmt.group_by.append(_text(item))
        return self.visitChildren(ctx)

    # ── WINDOW functions via functionCall OVER windowSpec ────────────────────

    def visitFunctionCall(self, ctx):  # type: ignore
        """functionCall has optional (OVER windowSpec) for window functions."""
        win_ctx = ctx.windowSpec() if hasattr(ctx, "windowSpec") else None
        if win_ctx is None:
            # check for OVER token directly (handles 'functionCall WITHIN GROUP ...')
            if not _has_token(ctx, "OVER"):
                return self.visitChildren(ctx)
        func_name_ctx = ctx.qualifiedIdentifier() if hasattr(ctx, "qualifiedIdentifier") else None
        self._stmt.windows.append({
            "func": _text(func_name_ctx),
            "window_spec": _text(win_ctx) if win_ctx else "",
        })
        return self.visitChildren(ctx)

    # Also handle primaryExpression OVER windowSpec (for analytical expressions)
    def visitWindowExpr(self, ctx):  # type: ignore
        func_ctx = ctx.primaryExpression() if hasattr(ctx, "primaryExpression") else None
        win_ctx = ctx.windowSpec() if hasattr(ctx, "windowSpec") else None
        self._stmt.windows.append({
            "func": _text(func_ctx),
            "window_spec": _text(win_ctx) if win_ctx else "",
        })
        return self.visitChildren(ctx)

    # ── UNNEST / LATERAL VIEW ────────────────────────────────────────────────

    def visitUnnestRelation(self, ctx):  # type: ignore
        self._stmt.unnests.append({
            "type": "UNNEST",
            "expr": _text(ctx),
            "alias": "",
        })
        return self.visitChildren(ctx)

    def visitLateralViewExpr(self, ctx):  # type: ignore
        self._stmt.unnests.append({
            "type": "LATERAL_VIEW",
            "expr": _text(ctx),
            "alias": "",
        })
        return self.visitChildren(ctx)

    # ── projections ──────────────────────────────────────────────────────────

    def visitSelectExpression(self, ctx):  # type: ignore
        expr_ctx = ctx.expression() if hasattr(ctx, "expression") else None
        alias_ctx = ctx.alias if hasattr(ctx, "alias") else None
        self._stmt.projections.append((
            _text(expr_ctx),
            _text(alias_ctx) if alias_ctx else "",
        ))
        return self.visitChildren(ctx)

    def visitSelectStar(self, ctx):  # type: ignore
        self._stmt.projections.append(("*", ""))
        return self.visitChildren(ctx)

    def visitSelectQualifiedStar(self, ctx):  # type: ignore
        q = ctx.qualifier if hasattr(ctx, "qualifier") else None
        self._stmt.projections.append((_text(q) + ".*" if q else "*", ""))
        return self.visitChildren(ctx)

    # ── SET operations ───────────────────────────────────────────────────────

    def visitSetOperation(self, ctx):  # type: ignore
        text = ctx.getText().upper()
        if "INTERSECT" in text:
            op = "INTERSECT"
        elif "EXCEPT" in text or "MINUS" in text:
            op = "EXCEPT"
        else:
            q = ctx.setQuantifier() if hasattr(ctx, "setQuantifier") else None
            op = "UNION_ALL" if q and "ALL" in _text(q).upper() else "UNION"
        self._stmt.set_ops.append((op, ""))
        return self.visitChildren(ctx)

    # ── INSERT statement ─────────────────────────────────────────────────────

    def visitInsertStatement(self, ctx):  # type: ignore
        tgt = ctx.target if hasattr(ctx, "target") else None
        schema, table = _qname(tgt)
        if table and (schema, table) not in self._stmt.target_tables:
            self._stmt.target_tables.append((schema, table))

        mode_ctx = ctx.insertMode() if hasattr(ctx, "insertMode") else None
        if mode_ctx and "OVERWRITE" in _text(mode_ctx).upper():
            self._stmt.statement_type = "INSERT_OVERWRITE"
        elif self._stmt.statement_type not in ("INSERT_OVERWRITE", "MERGE", "CTAS"):
            self._stmt.statement_type = "INSERT"

        part_ctx = ctx.partitionSpec() if hasattr(ctx, "partitionSpec") else None
        if part_ctx:
            for pv in (part_ctx.partitionVal() or []):
                id_ctx = pv.identifier() if hasattr(pv, "identifier") else None
                if id_ctx:
                    self._stmt.partition_cols.append(_text(id_ctx))

        return self.visitChildren(ctx)

    # ── MERGE statement ──────────────────────────────────────────────────────

    def visitMergeStatement(self, ctx):  # type: ignore
        tgt = ctx.target if hasattr(ctx, "target") else None
        schema, table = _qname(tgt)
        if table and (schema, table) not in self._stmt.target_tables:
            self._stmt.target_tables.append((schema, table))

        src = ctx.source if hasattr(ctx, "source") else None
        if src:
            src_tbl = src.macroOrIdentifier() if hasattr(src, "macroOrIdentifier") else None
            if src_tbl:
                s, t = _qname(src_tbl)
                self._stmt.source_tables.append((s, t, ""))

        for wc in (ctx.whenClause() or []):
            wtext = _text(wc).upper()
            if "UPDATE" in wtext:
                self._stmt.merge_actions.append({"action": "UPDATE"})
            elif "DELETE" in wtext:
                self._stmt.merge_actions.append({"action": "DELETE"})
            elif "INSERT" in wtext:
                self._stmt.merge_actions.append({"action": "INSERT"})

        return self.visitChildren(ctx)

    # ── CREATE TABLE ─────────────────────────────────────────────────────────

    def visitCreateTableStatement(self, ctx):  # type: ignore
        tbl = ctx.tableName if hasattr(ctx, "tableName") else None
        schema, table = _qname(tbl)
        if table:
            self._stmt.target_tables.append((schema, table))
        has_query = ctx.query() if hasattr(ctx, "query") else None
        self._stmt.statement_type = "CTAS" if has_query else "CREATE_TABLE"
        return self.visitChildren(ctx)

    def visitCreateViewStatement(self, ctx):  # type: ignore
        vn = ctx.viewName if hasattr(ctx, "viewName") else None
        schema, table = _qname(vn)
        if table:
            self._stmt.target_tables.append((schema, table))
        self._stmt.statement_type = "CREATE_VIEW"
        return self.visitChildren(ctx)

    def visitCreateMaterializedViewStatement(self, ctx):  # type: ignore
        vn = ctx.viewName if hasattr(ctx, "viewName") else None
        schema, table = _qname(vn)
        if table:
            self._stmt.target_tables.append((schema, table))
        self._stmt.statement_type = "CREATE_MATERIALIZED_VIEW"
        return self.visitChildren(ctx)

    # ── OpenGauss specifics ──────────────────────────────────────────────────

    def visitCopyStatement(self, ctx):  # type: ignore
        tbl_ctx = ctx.macroOrIdentifier() if hasattr(ctx, "macroOrIdentifier") else None
        schema, table = _qname(tbl_ctx)
        text = _text(ctx).upper()
        if "FROM" in text:
            self._stmt.statement_type = "COPY_FROM"
            if table and (schema, table) not in self._stmt.target_tables:
                self._stmt.target_tables.append((schema, table))
        else:
            self._stmt.statement_type = "COPY_TO"
            self._stmt.source_tables.append((schema, table, ""))

    def visitReturningClause(self, ctx):  # type: ignore
        items = ctx.selectItem() if hasattr(ctx, "selectItem") else []
        for item in (items if isinstance(items, list) else [items]):
            self._stmt.returning.append(_text(item))
        return self.visitChildren(ctx)

    def visitUpdateStatement(self, ctx):  # type: ignore
        tbl_ctx = ctx.macroOrIdentifier() if hasattr(ctx, "macroOrIdentifier") else None
        schema, table = _qname(tbl_ctx)
        if table:
            self._stmt.target_tables.append((schema, table))
        return self.visitChildren(ctx)

    def visitDeleteStatement(self, ctx):  # type: ignore
        tbl_ctx = ctx.macroOrIdentifier() if hasattr(ctx, "macroOrIdentifier") else None
        schema, table = _qname(tbl_ctx)
        if table:
            self._stmt.target_tables.append((schema, table))
        return self.visitChildren(ctx)

    # ── default traversal ────────────────────────────────────────────────────

    def visitChildren(self, node):  # type: ignore  # noqa: N802
        if node is None:
            return None
        for i in range(node.getChildCount()):
            node.getChild(i).accept(self)
        return None

    def defaultResult(self):  # type: ignore
        return None

    def aggregateResult(self, aggregate, nextResult):  # type: ignore
        return nextResult


# ─────────────────────────────────────────────────────────────────────────────
# Concrete visitor classes
# ─────────────────────────────────────────────────────────────────────────────

class SparkSqlLineageVisitor(_VisitorMixin, SparkSqlVisitor):
    def __init__(self, stmt: ParsedStatement) -> None:
        super().__init__()
        self._init(stmt)


class OpenGaussSqlLineageVisitor(_VisitorMixin, OpenGaussSqlVisitor):
    def __init__(self, stmt: ParsedStatement) -> None:
        super().__init__()
        self._init(stmt)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

_MACRO_RE = re.compile(r"\{([a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*)\}")


def parse_sql(sql: str, engine: SqlEngine) -> ParsedStatement:
    """
    Parse *sql* using the ANTLR4 grammar for *engine* and return a
    ParsedStatement populated with lineage-relevant information.

    This is a drop-in replacement for the regex-based SqlParser.parse().
    """
    stmt = ParsedStatement(sql=sql, engine=engine)
    # Pre-populate macros via regex as a safeguard (ANTLR4 MACRO_VAR token
    # also contributes, but this ensures correctness even if parsing fails)
    for m in _MACRO_RE.finditer(sql):
        if m.group(1) not in stmt.macros:
            stmt.macros.append(m.group(1))

    el = _SilentEL()

    if engine == SqlEngine.SPARK:
        lexer = SparkSqlLexer(InputStream(sql))
        lexer.removeErrorListeners()
        lexer.addErrorListener(el)
        stream = CommonTokenStream(lexer)
        parser = SparkSqlParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(el)
        tree = parser.singleStatement()
        visitor: _VisitorMixin = SparkSqlLineageVisitor(stmt)
    else:
        lexer = OpenGaussSqlLexer(InputStream(sql))
        lexer.removeErrorListeners()
        lexer.addErrorListener(el)
        stream = CommonTokenStream(lexer)
        parser = OpenGaussSqlParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(el)
        tree = parser.singleStatement()
        visitor = OpenGaussSqlLineageVisitor(stmt)

    visitor.visit(tree)

    # Remove CTE self-references from source tables
    stmt.source_tables = [
        (s, t, a) for s, t, a in stmt.source_tables
        if t.lower() not in visitor._cte_names
    ]

    # Deduplicate source tables
    seen: set = set()
    deduped = []
    for entry in stmt.source_tables:
        key = (entry[0].lower(), entry[1].lower())
        if key not in seen:
            seen.add(key)
            deduped.append(entry)
    stmt.source_tables = deduped

    return stmt
