"""SQL-only write profile. Never imported by the existing SELECT runner.

No filenames, network addresses, commands, role changes or runtime settings are
student-selectable. Isolation is still enforced by PostgreSQL roles and Docker.
"""

from pglast import ast, parse_sql
from pglast.parser import ParseError
from sql_runner.app.policy import (
    FUNCTIONS,
    TYPES,
    OPERATORS,
    NODES,
    SYSTEM_COLUMNS,
    names,
    PolicyError,
)

TABLES = {"users", "orders", "products", "order_items", "inventory", "reservations"}
WRITABLE = {"orders", "inventory", "reservations"}
EXTRA = {
    "InsertStmt",
    "UpdateStmt",
    "DeleteStmt",
    "TransactionStmt",
    "DefElem",
    "LockingClause",
    "OnConflictClause",
    "InferClause",
    "IndexElem",
    "ExplainStmt",
}


def validate_script(source):
    if not source.strip() or "\x00" in source or len(source.encode("utf-8")) > 32768:
        raise PolicyError("Expected 1–32768 UTF-8 bytes")
    try:
        statements = parse_sql(source)
    except ParseError:
        raise PolicyError("Invalid PostgreSQL syntax") from None
    if not 1 <= len(statements) <= 16:
        raise PolicyError("Expected 1–16 bounded statements")
    visited = 0

    def walk(node, scope=frozenset(), depth=0):
        nonlocal visited
        if node is None or isinstance(node, (str, int, float, bool)):
            return
        visited += 1
        if visited > 2000 or depth > 50:
            raise PolicyError("SQL complexity limit")
        if isinstance(node, (tuple, list)):
            for child in node:
                walk(child, scope, depth + 1)
            return
        if not isinstance(node, ast.Node) or type(node).__name__ not in NODES | EXTRA:
            raise PolicyError("Unsupported transaction construct")
        if isinstance(node, ast.TransactionStmt):
            if int(node.kind) not in range(7) or node.chain:
                raise PolicyError("Only BEGIN/COMMIT/ROLLBACK/SAVEPOINT supported")
            for option in node.options or ():
                if (
                    option.defname != "transaction_isolation"
                    or not isinstance(option.arg, ast.A_Const)
                    or option.arg.val.sval
                    not in {"read committed", "repeatable read", "serializable"}
                ):
                    raise PolicyError("Unsupported transaction option")
            return
        if (
            isinstance(node, (ast.InsertStmt, ast.UpdateStmt, ast.DeleteStmt))
            and node.relation.relname not in WRITABLE
        ):
            raise PolicyError("This table is not writable in this profile")
        if isinstance(node, ast.ExplainStmt):
            if not isinstance(node.query, ast.SelectStmt) or node.query.lockingClause:
                raise PolicyError("EXPLAIN supports read-only SELECT only")
            if node.options:
                raise PolicyError("Use plain EXPLAIN in this bounded profile")
        if isinstance(
            node, (ast.SelectStmt, ast.InsertStmt, ast.UpdateStmt, ast.DeleteStmt)
        ):
            if isinstance(node, ast.SelectStmt) and node.intoClause:
                raise PolicyError("SELECT INTO forbidden")
            visible = set(scope)
            if node.withClause:
                for cte in node.withClause.ctes:
                    if cte.search_clause or cte.cycle_clause:
                        raise PolicyError("SEARCH/CYCLE unsupported")
                    walk(
                        cte.ctequery,
                        frozenset(
                            visible
                            | ({cte.ctename} if node.withClause.recursive else set())
                        ),
                        depth + 1,
                    )
                    visible.add(cte.ctename)
            for field in node:
                if field != "withClause":
                    walk(getattr(node, field), frozenset(visible), depth + 1)
            return
        if isinstance(node, ast.RangeVar) and (
            node.catalogname
            or node.schemaname not in (None, "lab")
            or (
                node.relname not in TABLES
                and not (node.schemaname is None and node.relname in scope)
            )
        ):
            raise PolicyError("Only lab tables and visible CTEs permitted")
        if isinstance(node, ast.FuncCall):
            fn = names(node.funcname)
            if (
                len(fn) not in (1, 2)
                or (len(fn) == 2 and fn[0] != "pg_catalog")
                or fn[-1] not in FUNCTIONS
            ):
                raise PolicyError("Function forbidden")
        if isinstance(node, ast.TypeName):
            typ = names(node.names)
            if (
                len(typ) not in (1, 2)
                or (len(typ) == 2 and typ[0] != "pg_catalog")
                or typ[-1] not in TYPES
                or node.arrayBounds
                or node.setof
                or node.pct_type
            ):
                raise PolicyError("Type forbidden")
        if (
            isinstance(node, ast.A_Expr)
            and node.name
            and (len(node.name) != 1 or node.name[0].sval not in OPERATORS)
        ):
            raise PolicyError("Operator forbidden")
        if isinstance(node, ast.SortBy) and node.useOp:
            raise PolicyError("Custom sort operators forbidden")
        if isinstance(node, ast.ColumnRef):
            fields = names(tuple(f for f in node.fields if isinstance(f, ast.String)))
            if any(f in SYSTEM_COLUMNS for f in fields) or len(node.fields) > 2:
                raise PolicyError("System columns forbidden")
        for field in node:
            walk(getattr(node, field), scope, depth + 1)

    for statement in statements:
        if not isinstance(
            statement.stmt,
            (
                ast.SelectStmt,
                ast.InsertStmt,
                ast.UpdateStmt,
                ast.DeleteStmt,
                ast.TransactionStmt,
                ast.ExplainStmt,
            ),
        ):
            raise PolicyError("Statement forbidden")
        walk(statement.stmt)
    return statements
