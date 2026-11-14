from copy import deepcopy

import pytest

from sql_runner.app.comparator import compare


def result(rows, types=("text",), names=None, **fields):
    return dict(columns=[dict(name=name, pg_type=kind, type_oid=0) for name, kind in
                         zip(names or [f"c{i}" for i in range(len(types))], types)],
                rows=rows, rows_returned=len(rows), error=None, truncated=False, has_more=False, **fields)


def test_bag_counts_duplicates_and_order_is_a_separate_contract():
    expected = result([["A"], ["A"], ["B"]])
    assert compare(expected, result([["B"], ["A"], ["A"]])) == "passed"
    assert compare(expected, result([["A"], ["B"], ["B"]])) == "rows"
    assert compare(expected, result([["A"], ["B"]])) == "rows"
    assert compare(expected, result([["B"], ["A"], ["A"]]), comparison="ordered") == "rows"


@pytest.mark.parametrize("a,b", [(None, ""), (None, "NULL"), ("", "NULL"), ("a", "A"), (" a", "a")])
def test_null_empty_text_and_whitespace_remain_distinct(a, b):
    assert compare(result([[a]]), result([[b]])) == "rows"


@pytest.mark.parametrize("a,b", [
    ("9007199254740993", "9007199254740992"),
    ("12345678901234567890.012300", "12345678901234567890.012301"),
    ("0.00000000000000000000001", "0"),
])
def test_exact_numeric_precision(a, b):
    assert compare(result([[a]], ("numeric",)), result([[b]], ("numeric",))) == "rows"


def test_numeric_scale_compatibility_is_explicit_and_bool_is_not_one():
    assert compare(result([["100.00"]], ("numeric",)), result([["100.0"]], ("numeric",))) == "passed"
    expected, actual = result([["100"]], ("int8",)), result([["100.00"]], ("numeric",))
    assert compare(expected, actual) == "types"
    assert compare(expected, actual, numeric_compatible=True) == "passed"
    assert compare(result([["1"]], ("int8",)), result([[True]], ("bool",)), numeric_compatible=True) == "types"
    assert compare(expected, result([["100.0"]], ("float8",)), numeric_compatible=True) == "types"


@pytest.mark.parametrize("kind,value", [("bool", False), ("date", "2026-01-01"),
    ("timestamptz", "2026-01-01T00:00:00Z"), ("uuid", "00000000-0000-0000-0000-000000000000"),
    ("numeric", "NaN"), ("numeric", "Infinity"), ("float8", "-Infinity")])
def test_supported_typed_wire_values(kind, value):
    assert compare(result([[value]], (kind,)), result([[value]], (kind,))) == "passed"


def test_columns_order_aliases_and_zero_rows_are_still_checked():
    expected = result([], ("int8", "text"), ["user_id", "email"])
    assert compare(expected, deepcopy(expected)) == "passed"
    for names in [["id", "email"], ["email", "user_id"], ["user_id", "user_id"]]:
        assert compare(expected, result([], ("int8", "text"), names)) == "columns"
    assert compare(result([["A", "B"]], ("text", "text"), ["x", "x"]),
                   result([["B", "A"]], ("text", "text"), ["x", "x"])) == "rows"


@pytest.mark.parametrize("flag", ["has_more", "truncated"])
def test_matching_truncated_prefix_never_passes(flag):
    expected = result([["A"]])
    actual = deepcopy(expected); actual[flag] = True
    assert compare(expected, actual) == "result_limit"
    with pytest.raises(ValueError, match="Reference"):
        compare(actual, expected)


@pytest.mark.parametrize("error,code", [
    ({"kind": "postgres", "sqlstate": "22012"}, "sql_error"),
    ({"kind": "postgres", "sqlstate": "57014"}, "timeout"),
    ({"kind": "resource", "code": "query_deadline"}, "timeout"),
    ({"kind": "resource", "code": "output_limit"}, "result_limit"),
])
def test_errors_cannot_equal_a_correct_result(error, code):
    expected = result([["A"]]); actual = result([]); actual["error"] = error
    assert compare(expected, actual) == code


def test_malformed_protocol_and_unsupported_types_fail_closed():
    expected = result([["A"]])
    for actual in [result([[True]]), result([["A", "B"]]), result([["A"]], ("jsonb",))]:
        with pytest.raises(ValueError):
            compare(expected, actual)


def test_ordered_timestamp_ties_keep_exact_bigint_positions():
    rows = [["9007199254740993", "2026-10-01T00:00:00.123456Z"],
            ["9007199254740992", "2026-10-01T00:00:00.123456Z"]]
    expected = result(rows, ("int8", "timestamptz"), ["id", "created_at"])
    assert compare(expected, deepcopy(expected), comparison="ordered", numeric_compatible=True) == "passed"
    assert compare(expected, result(rows[::-1], ("int8", "timestamptz"), ["id", "created_at"]), comparison="ordered") == "rows"
    changed = deepcopy(expected); changed["rows"][0][1] = "2026-10-01T00:00:00.123455Z"
    assert compare(expected, changed, comparison="ordered") == "rows"
    wrong_type = result(rows, ("int8", "timestamp"), ["id", "created_at"])
    assert compare(expected, wrong_type, comparison="ordered") == "types"


def test_ordered_distinct_empty_null_duplicates_and_zero_rows():
    expected = result([[""], ["AA"], ["NULL"], ["ZZ"]], names=["country"])
    for rows in [[["AA"], [""], ["NULL"], ["ZZ"]], [[None], ["AA"], ["NULL"], ["ZZ"]],
                 [[""], ["AA"], ["AA"], ["NULL"], ["ZZ"]]]:
        assert compare(expected, result(rows, names=["country"]), comparison="ordered") == "rows"
    empty = result([], names=["country"])
    assert compare(empty, empty, comparison="ordered") == "passed"
    incomplete = deepcopy(expected); incomplete["has_more"] = True
    assert compare(expected, incomplete, comparison="ordered") == "result_limit"
