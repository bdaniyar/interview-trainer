"""Translate narrowly allowed CREATE INDEX syntax into a small immutable design."""
from dataclasses import dataclass
from typing import Literal

from pglast import ast, parse_sql
from pglast.parser import ParseError
from pglast.stream import RawStream

from sql_runner.app.policy import PolicyError, names, validate

COLUMNS = {
    "users": frozenset({"id", "email", "region"}),
    "orders": frozenset({"id", "user_id", "hotel_id", "arrival", "created_at", "status", "total"}),
}


@dataclass(frozen=True)
class Key:
    field: str
    expression: Literal["column", "lower"] = "column"
    descending: bool = False


@dataclass(frozen=True)
class Index:
    table: str
    keys: tuple[Key, ...]
    includes: tuple[str, ...]
    active_only: bool


def checked_parse(source, maximum):
    try:
        size = len(source.encode())
    except UnicodeError:
        raise PolicyError("Invalid UTF-8 SQL") from None
    if not source.strip() or "\x00" in source or size > 32768:
        raise PolicyError("Use 1–32768 UTF-8 bytes")
    try:
        statements = parse_sql(source)
    except ParseError:
        raise PolicyError("Invalid PostgreSQL syntax") from None
    if not 1 <= len(statements) <= maximum:
        raise PolicyError("Too many SQL statements")
    return tuple(item.stmt for item in statements)


def is_column(node, name):
    return isinstance(node, ast.ColumnRef) and len(node.fields) == 1 and (
        isinstance(node.fields[0], ast.String) and node.fields[0].sval == name
    )


def is_new(node):
    if isinstance(node, ast.TypeCast):
        cast = node.typeName
        if names(cast.names) not in {("text",), ("pg_catalog", "text")} or cast.arrayBounds or cast.typmods:
            return False
        node = node.arg
    return isinstance(node, ast.A_Const) and (
        isinstance(node.val, ast.String) and node.val.sval == "new"
    )


def predicate(node):
    if node is None:
        return False
    if (isinstance(node, ast.A_Expr) and int(node.kind) == 0 and names(node.name) == ("=",)
            and ((is_column(node.lexpr, "status") and is_new(node.rexpr))
                 or (is_column(node.rexpr, "status") and is_new(node.lexpr)))):
        return True
    raise PolicyError("Partial indexes may use status = 'new' in this lab")


def index_key(elem, table, *, include=False):
    if any(getattr(elem, field) for field in ("collation", "opclass", "opclassopts", "indexcolname")):
        raise PolicyError("Custom collations and operator classes are unavailable")
    if int(elem.nulls_ordering) != 0 or int(elem.ordering) not in (0, 1, 2):
        raise PolicyError("Use the default NULL ordering")
    if elem.name in COLUMNS[table] and elem.expr is None:
        return Key(elem.name, descending=int(elem.ordering) == 2)
    fn = elem.expr
    if include or table != "users" or not isinstance(fn, ast.FuncCall):
        raise PolicyError("Use a supported index key")
    if (names(fn.funcname) not in {("lower",), ("pg_catalog", "lower")}
            or len(fn.args or ()) != 1 or not is_column(fn.args[0], "email")
            or any(getattr(fn, field) for field in ("agg_order", "agg_filter", "over",
                       "agg_within_group", "agg_star", "agg_distinct", "func_variadic"))):
        raise PolicyError("The only supported expression is lower(email)")
    return Key("email", expression="lower", descending=int(elem.ordering) == 2)


def indexes(source):
    design = []
    for node in checked_parse(source, 2):
        if not isinstance(node, ast.IndexStmt):
            raise PolicyError("Only a bounded CREATE INDEX design is accepted")
        relation = node.relation
        table = relation.relname
        if (relation.catalogname or relation.schemaname not in (None, "lab") or table not in COLUMNS
                or node.accessMethod not in (None, "btree") or not 1 <= len(node.indexParams or ()) <= 3
                or len(node.indexIncludingParams or ()) > 2):
            raise PolicyError("Use at most three approved B-tree keys on users or orders")
        allowed = {"idxname", "relation", "accessMethod", "indexParams", "indexIncludingParams",
                   "whereClause", "if_not_exists"}
        if any(getattr(node, field) for field in node if field not in allowed):
            raise PolicyError("Index storage, unique, concurrency and other options are disabled")
        keys = tuple(index_key(elem, table) for elem in node.indexParams)
        includes = tuple(index_key(elem, table, include=True).field for elem in node.indexIncludingParams or ())
        if len(set(keys)) != len(keys) or set(includes) & {key.field for key in keys} or len(set(includes)) != len(includes):
            raise PolicyError("Index keys and included columns must be distinct")
        active_only = predicate(node.whereClause)
        if active_only and table != "orders":
            raise PolicyError("Only orders has a status predicate")
        design.append(Index(table, keys, includes, active_only))
    return tuple(design)


def select_node(node):
    if not isinstance(node, ast.SelectStmt):
        raise PolicyError("Expected a read-only SELECT")
    statement = RawStream()(node)
    validate(statement)
    return statement


def select(source):
    node, = checked_parse(source, 1)
    return select_node(node)


def plan_submission(source, *, estimate_allowed):
    node, = checked_parse(source, 1)
    if not isinstance(node, ast.ExplainStmt):
        raise PolicyError("Submit EXPLAIN with one SELECT")
    options = {}
    boolean = {"on", "true", "off", "false"}
    for item in node.options or ():
        if item.defname not in {"analyze", "buffers", "timing", "format"} or item.defname in options:
            raise PolicyError("Unsupported EXPLAIN option")
        options[item.defname] = (
            item.arg.sval.lower() if isinstance(item.arg, ast.String) else
            "true" if item.arg is None else ""
        )
    if (options.get("analyze", "false") not in boolean
            or options.get("buffers", "false") not in boolean
            or options.get("timing", "false") not in {"off", "false"}
            or options.get("format", "json") not in {"json", "text"}):
        raise PolicyError("Unsupported EXPLAIN options")
    analyze = options.get("analyze") in {"on", "true"}
    buffers = options.get("buffers") in {"on", "true"}
    if not ((analyze and buffers) or (estimate_allowed and not analyze and not buffers)):
        raise PolicyError("For execution and Check, include ANALYZE and BUFFERS")
    return select_node(node.query), analyze
