"""PostgreSQL 17 grammar, recursively checked against a small capability set.

This is an admission policy, not the isolation boundary. Database privileges,
peer authentication, containers and independent deadlines remain mandatory.
"""
from pglast import ast, parse_sql
from pglast.parser import ParseError

from .config import SQL_BYTES
from .datasets import TABLES

FUNCTIONS = frozenset({
    "count", "sum", "min", "max", "avg", "lower", "upper", "length",
    "abs", "round", "ceil", "floor", "row_number", "rank", "dense_rank",
    "lag", "lead", "first_value", "last_value", "nth_value",
    "repeat", "generate_series",
})
TYPES = frozenset({"bool", "text", "varchar", "bpchar", "int2", "int4", "int8",
                   "numeric", "float4", "float8", "date", "time", "timetz",
                   "timestamp", "timestamptz", "interval", "uuid"})
NODES = frozenset({
    "SelectStmt", "ResTarget", "ColumnRef", "A_Star", "A_Const", "Integer",
    "Float", "String", "Boolean", "A_Expr", "BoolExpr", "BooleanTest",
    "NullTest", "CaseExpr", "CaseWhen", "CoalesceExpr", "MinMaxExpr",
    "RangeVar", "RangeSubselect", "RangeFunction", "JoinExpr", "Alias",
    "SortBy", "SubLink", "TypeCast", "TypeName", "FuncCall", "WindowDef",
})
OPERATORS = frozenset({"=", "<>", "!=", "<", ">", "<=", ">=", "+", "-", "*",
                       "/", "%", "^", "||", "~~", "!~~", "~~*", "!~~*"})
SYSTEM_COLUMNS = frozenset({"ctid", "tableoid", "xmin", "xmax", "cmin", "cmax"})


class PolicyError(ValueError):
    def __init__(self, message, *, code="unsupported_sql", position=None,
                 sqlstate=None):
        super().__init__(message)
        self.code, self.position, self.sqlstate = code, position, sqlstate


def names(items):
    return tuple(item.sval for item in items or ())


def validate(sql: str) -> None:
    try:
        byte_size = len(sql.encode("utf-8"))
    except UnicodeEncodeError:
        raise PolicyError("SQL must be valid UTF-8", code="sql_size") from None
    if not sql.strip() or "\x00" in sql or byte_size > SQL_BYTES:
        raise PolicyError("SQL must contain 1–32768 UTF-8 bytes without NUL", code="sql_size")
    try:
        statements = parse_sql(sql)
    except ParseError as exc:
        # pglast reports a zero-based character index, including Unicode input.
        index = exc.args[1] if len(exc.args) > 1 else None
        position = index + 1 if index is not None else len(sql) + 1
        raise PolicyError(str(exc.args[0]), code="syntax_error", position=position,
                          sqlstate="42601") from None
    if len(statements) != 1 or not isinstance(statements[0].stmt, ast.SelectStmt):
        raise PolicyError("Only one SELECT statement is supported")
    visited = 0

    def walk(node, scope=frozenset(), depth=0):
        nonlocal visited
        if node is None or isinstance(node, (str, int, float, bool)):
            return
        visited += 1
        if visited > 2000 or depth > 50:
            raise PolicyError("SQL expression is too complex", code="sql_complexity")
        if isinstance(node, (tuple, list)):
            for item in node:
                walk(item, scope, depth + 1)
            return
        kind = type(node).__name__
        if not isinstance(node, ast.Node) or kind not in NODES:
            raise PolicyError(f"Unsupported SQL construct: {kind}")
        if isinstance(node, ast.SelectStmt):
            if node.intoClause or node.lockingClause:
                raise PolicyError("SELECT INTO and row locks are forbidden")
            visible = set(scope)
            if node.withClause:
                for cte in node.withClause.ctes:
                    if not isinstance(cte.ctequery, ast.SelectStmt) or cte.search_clause or cte.cycle_clause:
                        raise PolicyError("Only read-only CTEs without SEARCH/CYCLE are supported")
                    cte_scope = visible | ({cte.ctename} if node.withClause.recursive else set())
                    walk(cte.ctequery, frozenset(cte_scope), depth + 1)
                    visible.add(cte.ctename)
            for field in node:
                if field != "withClause":
                    walk(getattr(node, field), frozenset(visible), depth + 1)
            return
        if isinstance(node, ast.RangeVar):
            if (node.catalogname or node.schemaname not in (None, "lab")
                    or (node.relname not in TABLES and
                        not (node.schemaname is None and node.relname in scope))):
                raise PolicyError("Only shop-v1 tables and visible CTEs are accessible")
        if isinstance(node, ast.FuncCall):
            fn = names(node.funcname)
            if len(fn) not in (1, 2) or (len(fn) == 2 and fn[0] != "pg_catalog") or fn[-1] not in FUNCTIONS:
                raise PolicyError("Function is outside the SELECT allowlist")
        if isinstance(node, ast.TypeName):
            tn = names(node.names)
            if (len(tn) not in (1, 2) or (len(tn) == 2 and tn[0] != "pg_catalog")
                    or tn[-1] not in TYPES or node.arrayBounds or node.setof or node.pct_type):
                raise PolicyError("Type is outside the scalar type allowlist")
        if isinstance(node, ast.A_Expr) and node.name:
            if len(node.name) != 1 or node.name[0].sval not in OPERATORS:
                raise PolicyError("Operator is outside the SELECT allowlist")
        if isinstance(node, ast.SortBy) and node.useOp:
            raise PolicyError("ORDER BY USING is unsupported")
        if isinstance(node, ast.ColumnRef):
            fields = names(tuple(f for f in node.fields if isinstance(f, ast.String)))
            if any(f in SYSTEM_COLUMNS for f in fields) or len(node.fields) > 2:
                raise PolicyError("System columns and cross-schema column references are forbidden")
        for field in node:
            walk(getattr(node, field), scope, depth + 1)

    walk(statements[0].stmt)
