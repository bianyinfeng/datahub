"""
ANTLR4-based SQL parsing toolkit supporting Spark SQL and OpenGauss/PostgreSQL dialects.

Features:
- Macro variable support ({macro_var}) in all SQL positions
- Operator-level JSON lineage (SCAN/UNNEST/FILTER/AGGREGATE/WINDOW/JOIN/SET/PROJECT/WRITE)
- Column-level, table-level, and statement-level lineage
- DataHub URN integration
"""

from datahub.sql_parsing.antlr4.antlr4_visitor import parse_sql
from datahub.sql_parsing.antlr4.parser import SqlParser  # legacy regex parser kept for compatibility
from datahub.sql_parsing.antlr4.lineage_builder import LineageBuilder
from datahub.sql_parsing.antlr4.models import (
    LineageGraph,
    OperatorNode,
    OperatorType,
    OperatorSubtype,
    SqlEngine,
)

__all__ = [
    "parse_sql",   # preferred: ANTLR4-based parser
    "SqlParser",   # legacy: regex-based parser
    "LineageBuilder",
    "LineageGraph",
    "OperatorNode",
    "OperatorType",
    "OperatorSubtype",
    "SqlEngine",
]
