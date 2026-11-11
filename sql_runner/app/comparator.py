"""Typed, bounded result comparison. No expected/student values in feedback."""
from collections import Counter
from decimal import Decimal, InvalidOperation

INTEGER = {"int2", "int4", "int8"}
FLOAT = {"float4", "float8"}
TEXT = {"text", "varchar", "bpchar"}
SCALARS = {"bool", "date", "time", "timetz", "timestamp", "timestamptz", "uuid", "interval"}


def family(pg_type, numeric_compatible):
    if pg_type in INTEGER:
        return "number" if numeric_compatible else "integer"
    if pg_type == "numeric":
        return "number" if numeric_compatible else "numeric"
    if pg_type in FLOAT:
        return "float"  # exact wire value, no implicit tolerance or numeric mixing
    if pg_type in TEXT:
        return "text"
    if pg_type in SCALARS:
        return pg_type
    raise ValueError("Unsupported comparator type")


def cell(value, kind):
    if value is None:
        return ("null",)
    if kind == "bool":
        if type(value) is not bool:
            raise ValueError("Invalid boolean wire value")
        return (kind, value)
    if not isinstance(value, str):
        raise ValueError("Invalid scalar wire value")
    if kind in {"number", "integer", "numeric", "float"}:
        try:
            number = Decimal(value)
        except InvalidOperation:
            raise ValueError("Invalid numeric wire value") from None
        if number.is_nan():
            return (kind, "NaN")
        return (kind, number)
    return (kind, value)


def normalized(result, numeric_compatible):
    columns = result["columns"]
    if result["rows_returned"] != len(result["rows"]):
        raise ValueError("Invalid row count")
    kinds = tuple(family(col["pg_type"], numeric_compatible) for col in columns)
    rows = []
    for row in result["rows"]:
        if len(row) != len(columns):
            raise ValueError("Invalid row shape")
        rows.append(tuple(cell(value, kind) for value, kind in zip(row, kinds)))
    return kinds, rows


def complete_reference(result):
    if result.get("error") or result.get("truncated") or result.get("has_more"):
        raise ValueError("Reference query did not produce a complete result")


def compare(expected, actual, *, comparison="unordered", numeric_compatible=False):
    complete_reference(expected)
    if comparison not in {"ordered", "unordered"}:
        raise ValueError("Unknown comparison contract")
    error = actual.get("error")
    if error:
        state = error.get("sqlstate") or ""
        if state in {"57014", "55P03", "25P04"} or error.get("code") == "query_deadline":
            return "timeout"
        if error.get("kind") == "resource" or state.startswith(("53", "54")):
            return "result_limit"
        return "sql_error"
    if actual.get("truncated") or actual.get("has_more"):
        return "result_limit"
    if [c["name"] for c in actual["columns"]] != [c["name"] for c in expected["columns"]]:
        return "columns"
    expected_types, expected_rows = normalized(expected, numeric_compatible)
    actual_types, actual_rows = normalized(actual, numeric_compatible)
    if actual_types != expected_types:
        return "types"
    equal = actual_rows == expected_rows if comparison == "ordered" else Counter(actual_rows) == Counter(expected_rows)
    return "passed" if equal else "rows"
