from decimal import Decimal
import json
from pathlib import Path
import re

import pytest

from sql_runner.app.comparator import compare
from sql_runner.tests.integration.test_order_distinct_grading import fixture, grade, run, task_for

COUNT = "SELECT COUNT(*) AS orders_count FROM orders"
GROUP = "SELECT status,COUNT(*) AS count FROM orders GROUP BY status ORDER BY status"
HAVING = "SELECT user_id,COUNT(*) AS count FROM orders GROUP BY user_id HAVING COUNT(*) >= 2 ORDER BY user_id"


@pytest.mark.parametrize("task_id,query", [
    ("sql.aggregation.09", COUNT),
    ("sql.aggregation.09", "select count(id) as orders_count from lab.orders"),
    ("sql.aggregation.10", GROUP),
    ("sql.aggregation.10", "select o.status,count(o.id) as count from lab.orders o group by 1 order by 1 asc"),
    ("sql.aggregation.13", HAVING),
    ("sql.aggregation.13", "WITH totals AS (SELECT user_id,COUNT(*) AS count FROM orders GROUP BY user_id) SELECT user_id,count FROM totals WHERE count >= 2 ORDER BY user_id"),
])
def test_correct_and_equivalent_aggregate_solutions_pass_six_cases(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert result["passed"] and result["tests_passed"] == result["tests_total"] == 6
    assert not manager.backend.containers()


def test_count_wrong_source_alias_missing_or_extra_rows_fail(manager):
    queries = ["SELECT COUNT(*) AS orders_count FROM users", "SELECT 5 AS orders_count",
        "SELECT COUNT(*) AS count FROM orders", "SELECT 1 AS orders_count FROM orders",
        COUNT + " GROUP BY id", COUNT + " UNION ALL " + COUNT,
        "SELECT COUNT(*) AS orders_count FROM orders WHERE status='paid'",
        "SELECT COUNT(DISTINCT user_id) AS orders_count FROM orders"]
    with fixture(manager, "sql.aggregation.09", "same-user-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert expected["rows"] == [["7"]]
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None
            assert compare(expected, actual, comparison=task.comparison, numeric_compatible=True) != "passed", query
    with fixture(manager, "sql.aggregation.09", "empty-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert expected["rows"] == [["0"]]
        for query in [COUNT + " GROUP BY status", "SELECT SUM(1) AS orders_count FROM orders"]:
            assert compare(expected, run(manager, handle, query), comparison="ordered", numeric_compatible=True) == "rows"


def test_grouping_missing_groups_wrong_keys_counts_or_row_order_fail(manager):
    queries = [
        "SELECT 'paid' AS status,COUNT(*) AS count FROM orders",
        "SELECT user_id::text AS status,COUNT(*) AS count FROM orders GROUP BY user_id ORDER BY user_id",
        "SELECT status,1 AS count FROM orders ORDER BY status",
        GROUP.replace("FROM orders", "FROM orders WHERE status='paid'"),
        GROUP.replace("COUNT(*)", "COUNT(DISTINCT user_id)"),
        GROUP + " DESC", GROUP.replace(" ORDER BY status", ""),
        "SELECT COUNT(*) AS count,status FROM orders GROUP BY status ORDER BY status",
    ]
    with fixture(manager, "sql.aggregation.10", "skewed-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert expected["rows"] == [["cancelled", "1"], ["new", "2"], ["paid", "4"]]
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None
            assert compare(expected, actual, comparison="ordered", numeric_compatible=True) != "passed", query


def test_having_one_two_three_boundary_count_and_order_are_distinguished(manager):
    queries = [HAVING.replace(">= 2", "> 2"), HAVING.replace(">= 2", "= 2"),
        HAVING.replace(">= 2", ">= 1"), HAVING.replace(" HAVING COUNT(*) >= 2", ""),
        HAVING.replace("COUNT(*) AS count", "COUNT(*)+1 AS count"), HAVING + " DESC",
        HAVING.replace("COUNT(*) AS count", "COUNT(DISTINCT status) AS count")]
    with fixture(manager, "sql.aggregation.13", "boundary-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert expected["rows"] == [["7", "2"], ["300", "3"]]
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None
            assert compare(expected, actual, comparison="ordered", numeric_compatible=True) != "passed", query


@pytest.mark.parametrize("task_id,query", [
    ("sql.aggregation.09", "SELECT COUNT(*) AS orders_count FROM users"),
    ("sql.aggregation.10", GROUP + " DESC"),
    ("sql.aggregation.13", HAVING.replace(">= 2", "> 2")),
])
def test_full_check_rejects_common_aggregate_mistakes(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] < 6
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,query", [
    ("sql.aggregation.09", "SELECT 5::bigint AS orders_count"),
    ("sql.aggregation.10", "SELECT * FROM (VALUES ('cancelled',1::bigint),('new',1::bigint),('paid',3::bigint)) v(status,count) ORDER BY status"),
    ("sql.aggregation.13", "SELECT * FROM (VALUES (1::bigint,2::bigint),(2::bigint,2::bigint)) v(user_id,count) ORDER BY user_id"),
])
def test_hardcoded_public_aggregates_pass_only_baseline(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] == 1
    assert not manager.backend.containers()


def test_new_fixture_results_are_independently_verified(manager):
    expected = {
        "sql.aggregation.09": {"public-v1": [["5"]], "empty-v1": [["0"]], "one-v1": [["1"]],
            "same-user-v1": [["7"]], "mixed-v1": [["6"]], "sparse-v1": [["2"]]},
        "sql.aggregation.10": {"public-v1": [["cancelled", "1"], ["new", "1"], ["paid", "3"]],
            "empty-v1": [], "single-status-v1": [["new", "6"]],
            "skewed-v1": [["cancelled", "1"], ["new", "2"], ["paid", "4"]],
            "equal-v1": [["cancelled", "2"], ["new", "2"], ["paid", "2"]],
            "shuffled-v1": [["cancelled", "2"], ["new", "3"], ["paid", "1"]]},
        "sql.aggregation.13": {"public-v1": [["1", "2"], ["2", "2"]], "empty-v1": [], "none-v1": [],
            "boundary-v1": [["7", "2"], ["300", "3"]],
            "several-v1": [["8", "2"], ["41", "3"], ["9007199254740993", "4"]],
            "single-qualifier-v1": [["23", "5"]]},
    }
    for task_id, cases in expected.items():
        for case_id, rows in cases.items():
            with fixture(manager, task_id, case_id) as (handle, task):
                result = run(manager, handle, task.reference_sql)
                assert result["error"] is None and not result["truncated"]
                assert result["rows"] == rows, (task_id, case_id, result["rows"])
                assert result["columns"][-1]["pg_type"] == "int8"


def test_postgresql_aggregate_null_types_empty_inputs_and_exact_numeric_values(manager, session):
    sid = session["session_id"]
    def query(sql):
        result = manager.run(sid, 1, sql)
        assert result["error"] is None and not result["truncated"]
        return result
    count = query("SELECT COUNT(*),COUNT(country),COUNT(DISTINCT country) FROM users")
    assert count["rows"] == [["4", "3", "2"]] and all(c["pg_type"] == "int8" for c in count["columns"])
    for where, rows_count in [("WHERE false", "0"), ("WHERE country IS NULL", "1")]:
        result = query("SELECT COUNT(*),COUNT(country),SUM(length(country)),AVG(length(country)),MIN(country),MAX(country) FROM users " + where)
        assert result["rows"] == [[rows_count, "0", None, None, None, None]]
    totals = query("SELECT SUM(total),AVG(total),MIN(total),MAX(total) FROM orders")
    assert [Decimal(x) for x in totals["rows"][0]] == [Decimal("470"), Decimal("94"), Decimal("40"), Decimal("200")]
    assert all(c["pg_type"] == "numeric" for c in totals["columns"])
    exact = query("SELECT SUM(n),AVG(n) FROM (VALUES (9007199254740993::bigint),(9007199254740993::bigint)) v(n)")
    assert Decimal(exact["rows"][0][0]) == Decimal("18014398509481986")
    assert Decimal(exact["rows"][0][1]) == Decimal("9007199254740993")
    assert all(c["pg_type"] == "numeric" for c in exact["columns"])
    decimal = query("SELECT SUM(n),AVG(n) FROM (VALUES (0.00000000000000000001::numeric),(0.00000000000000000003::numeric)) v(n)")
    assert [Decimal(x) for x in decimal["rows"][0]] == [Decimal('4e-20'),Decimal('2e-20')]


@pytest.mark.parametrize("task_id", ["sql.aggregation.09", "sql.aggregation.10", "sql.aggregation.13"])
def test_aggregate_check_keeps_explorer_read_only_and_feedback_safe(manager, session, task_id):
    sid = session["session_id"]
    catalog = manager.catalog(sid, 1)
    before = manager.run(sid, 1, "SELECT * FROM orders ORDER BY id")["rows"]
    assert grade(manager, task_id, task_for(task_id).reference_sql)["passed"]
    assert manager.catalog(sid, 1) == catalog
    assert manager.run(sid, 1, "SELECT * FROM orders ORDER BY id")["rows"] == before
    result = grade(manager, task_id, "SELECT SUM(email::bigint) AS orders_count FROM users")
    assert not result["passed"] and "@example" not in json.dumps(result)
    assert result["feedback"][0]["sqlstate"] == "22P02"
    for bad in ["DELETE FROM orders", "CREATE TABLE bad(x int)", "SELECT 1; SELECT 2"]:
        assert grade(manager, task_id, bad)["feedback"][0]["code"] == "policy"
    assert len(manager.backend.containers()) == 1


def test_aggregate_truncation_and_timeout_do_not_pass(manager):
    result = grade(manager, "sql.aggregation.10", "SELECT g::text AS status,COUNT(*) AS count FROM generate_series(1,501) g GROUP BY g")
    assert not result["passed"] and result["feedback"][0]["code"] == "result_limit"
    # ProjectSet streams the input; a FROM-function could hit temp_file_limit
    # before the statement timeout, exercising a different resource safeguard.
    result = grade(manager, "sql.aggregation.09", "SELECT SUM(g) AS orders_count FROM (SELECT generate_series(1,1000000000) g) s")
    assert not result["passed"] and result["feedback"][0]["code"] == "timeout"
    assert not manager.backend.containers()


# Golden values are authored independently of the queries in lesson.md. Numeric
# scale is formatting, so compare Decimals exactly; never round or use a tolerance.
LESSON_RESULTS = {
    "s10-aggregates": [
        [["4"]], [["4", "3", "2"]], [["470", "94", "40", "200"]],
        [["0", None, None, None, None]], [["0"]],
        [["1", "0", None, None, None, None]], [["3", "1"]], [["5"]],
        [["30", "90"]], [["350", "116.67"]],
    ],
    "s10-group-by": [
        [["books", "2", "70"], ["hardware", "1", "90"]],
        [["1", "2", "140"], ["2", "2", "250"], ["4", "1", "80"]],
        [["1", "cancelled", "1"], ["1", "paid", "1"], ["2", "paid", "2"], ["4", "new", "1"]],
        "42803",
        [["GE", "1", "1"], ["KZ", "2", "2"], [None, "1", "0"]],
        [["books"], ["hardware"]], [["books"], ["hardware"]],
        [["1", "100"], ["2", "250"]], [],
        [["cancelled", "40"], ["new", "80"], ["paid", "116.67"]],
        [["cancelled", "1"], ["new", "1"], ["paid", "3"]],
        [["116.6666666666666667"]],
    ],
    "s10-having": [
        [["books", "2"]],
        [["cancelled", "1", "40"], ["new", "1", "80"], ["paid", "3", "350"]],
        [["paid", "3", "350"]], [["2", "2", "250"]], "42803",
        [["1", "1", "100"], ["2", "1", "200"]],
        [["1", "2"], ["2", "2"]], [["hardware", "90"]],
    ],
}


@pytest.mark.parametrize("slug,expected", LESSON_RESULTS.items())
def test_all_curated_aggregation_lesson_blocks_and_stated_values(manager, session, slug, expected):
    source = (Path(__file__).resolve().parents[3] / "content" / "stage-10" / slug / "lesson.md").read_text()
    blocks = list(re.finditer(r"```sql\n(.*?)```", source, re.S))
    assert len(blocks) == len(expected)
    for block, golden in zip(blocks, expected):
        actual = manager.run(session["session_id"], 1, block[1])
        if isinstance(golden, str):
            assert "Намеренно ошибочный" in source[max(0, block.start() - 500):block.start()]
            assert actual["error"]["sqlstate"] == golden
            continue
        assert actual["error"] is None and not actual["truncated"], block[1]
        assert len(actual["rows"]) == len(golden), block[1]
        for row, wanted in zip(actual["rows"], golden):
            assert len(row) == len(wanted)
            for cell, value, column in zip(row, wanted, actual["columns"]):
                if cell is None or value is None:
                    assert cell is value
                elif column["pg_type"] in {"int2", "int4", "int8", "numeric"}:
                    assert Decimal(cell) == Decimal(value), (block[1], cell, value)
                else:
                    assert cell == value, (block[1], cell, value)
