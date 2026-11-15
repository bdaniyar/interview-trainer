from collections import Counter
import json

import pytest

from sql_runner.app.comparator import compare
from sql_runner.tests.integration.test_order_distinct_grading import fixture, grade, run, task_for

INNER = "SELECT o.id AS order_id,u.email FROM orders o JOIN users u ON u.id=o.user_id"
ANTI = "SELECT u.id,u.email FROM users u LEFT JOIN orders o ON o.user_id=u.id WHERE o.id IS NULL"
RIGHT = "SELECT p.id AS product_id,oi.order_id FROM order_items oi RIGHT JOIN products p ON p.id=oi.product_id ORDER BY p.id,oi.order_id"
SELF = "SELECT u.email,m.email AS manager_email FROM users u LEFT JOIN users m ON m.id=u.manager_id ORDER BY u.id"
FULL = "SELECT a.id AS left_id,a.label AS left_label,b.id AS right_id,b.label AS right_label FROM (VALUES (1,'local-only'),(2,'local-match')) a(id,label) FULL OUTER JOIN (VALUES (2,'remote-match'),(3,'remote-only')) b(id,label) ON a.id=b.id ORDER BY COALESCE(a.id,b.id)"


@pytest.mark.parametrize("task_id,query", [
    ("sql.join.17", INNER),
    ("sql.join.17", "SELECT sales.id AS order_id,customer.email FROM lab.users customer,lab.orders sales WHERE sales.user_id=customer.id ORDER BY sales.id DESC"),
    ("sql.join.18", ANTI),
    ("sql.join.18", "SELECT u.id,u.email FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.id) ORDER BY u.id DESC"),
    ("sql.join.25", RIGHT),
    ("sql.join.25", "SELECT p.id AS product_id,i.order_id FROM products p LEFT JOIN order_items i ON i.product_id=p.id ORDER BY 1,2"),
    ("sql.join.20", SELF),
    ("sql.join.20", "SELECT person.email,boss.email AS manager_email FROM users boss RIGHT JOIN users person ON person.manager_id=boss.id ORDER BY person.id"),
])
def test_correct_and_equivalent_join_solutions_pass_all_six_cases(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert result["passed"] and result["tests_passed"] == result["tests_total"] == 6
    assert not manager.backend.containers()


def assert_wrong_queries(manager, task_id, case_id, queries):
    with fixture(manager, task_id, case_id) as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None, (query, actual["error"])
            assert compare(expected, actual, comparison=task.comparison, numeric_compatible=True) != "passed", query


def test_inner_join_relationship_cardinality_aliases_and_bag_multiplicity(manager):
    assert_wrong_queries(manager, "sql.join.17", "repeated-owner-v1", [
        INNER.replace("u.id=o.user_id", "u.id=o.id"),
        "SELECT o.id AS order_id,u.email FROM orders o CROSS JOIN users u",
        "SELECT MIN(o.id) AS order_id,u.email FROM orders o JOIN users u ON u.id=o.user_id GROUP BY u.id,u.email",
        "SELECT o.id AS order_id,'wrong@example.test' AS email FROM orders o",
        INNER.replace("AS order_id", "AS id"),
        "SELECT u.email,o.id AS order_id FROM orders o JOIN users u ON u.id=o.user_id",
        INNER + " LIMIT 1", INNER + " UNION ALL " + INNER,
        INNER + " WHERE o.status='paid'",
    ])
    with fixture(manager, "sql.join.17", "crossed-ids-v1") as (handle, task):
        good = run(manager, handle, task.reference_sql)
        wrong = run(manager, handle, INNER.replace("u.id=o.user_id", "u.id=o.id"))
        assert len(wrong["rows"]) == 3 and compare(good, wrong, numeric_compatible=True) == "rows"
    with fixture(manager, "sql.join.17", "repeated-owner-v1") as (handle, task):
        result = run(manager, handle, task.reference_sql)
        assert Counter(row[1] for row in result["rows"])["repeat@example.test"] == 3
        # order_id is unique: DISTINCT over both selected fields is equivalent.
        assert compare(result, run(manager, handle, INNER.replace("SELECT ", "SELECT DISTINCT ", 1)), numeric_compatible=True) == "passed"


def test_anti_join_preserves_only_users_with_no_orders_without_duplication(manager):
    assert_wrong_queries(manager, "sql.join.18", "mixed-v1", [
        ANTI.replace("LEFT JOIN", "JOIN"), ANTI.replace("IS NULL", "IS NOT NULL"),
        ANTI.replace("o.id IS NULL", "u.country IS NULL"),
        ANTI.replace("o.id IS NULL", "u.id=3"), ANTI.replace(" WHERE o.id IS NULL", ""),
        ANTI.replace("o.user_id=u.id", "o.id=u.id"), ANTI + " UNION ALL " + ANTI,
        ANTI + " LIMIT 1", ANTI.replace("u.id,u.email", "u.id AS user_id,u.email"),
    ])
    with fixture(manager, "sql.join.18", "mixed-v1") as (handle, task):
        # Both columns are NOT NULL on a real match; neither spelling is forced.
        assert compare(run(manager, handle, task.reference_sql), run(manager, handle, ANTI.replace("o.id IS NULL", "o.user_id IS NULL")), numeric_compatible=True) == "passed"


def test_right_join_unsold_multi_match_nulls_column_order_and_sequence(manager):
    distinct_one = RIGHT.replace("SELECT ", "SELECT DISTINCT ON (p.id) ", 1)
    assert_wrong_queries(manager, "sql.join.25", "mixed-v1", [
        RIGHT.replace("RIGHT JOIN", "JOIN"), RIGHT.replace("RIGHT JOIN", "LEFT JOIN"),
        RIGHT.replace("p.id=oi.product_id", "p.id=oi.order_id"),
        RIGHT.replace("oi.order_id FROM", "COALESCE(oi.order_id,0) AS order_id FROM"),
        RIGHT.replace("oi.order_id FROM", "COALESCE(oi.order_id::text,'NULL') AS order_id FROM"),
        distinct_one, RIGHT.replace("ORDER BY p.id,oi.order_id", "ORDER BY p.id DESC,oi.order_id DESC"),
        RIGHT.replace("ORDER BY p.id,oi.order_id", "ORDER BY p.id,oi.order_id DESC"),
        RIGHT.replace(" ORDER BY p.id,oi.order_id", ""),
        RIGHT.replace("p.id AS product_id,oi.order_id", "oi.order_id,p.id AS product_id"),
        RIGHT + " LIMIT 1",
    ])
    with fixture(manager, "sql.join.25", "mixed-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert sum(row[0] == "700" for row in expected["rows"]) == 3
        assert sum(row[1] is None for row in expected["rows"]) == 2
        # Composite PK makes (product_id, order_id) unique. Only suppressing by
        # product alone loses matches; full-row DISTINCT must remain acceptable.
        assert compare(expected, run(manager, handle, RIGHT.replace("SELECT ", "SELECT DISTINCT ", 1)), comparison="ordered", numeric_compatible=True) == "passed"


def test_self_join_direction_roots_shared_manager_nulls_and_sorting(manager):
    assert_wrong_queries(manager, "sql.join.20", "hierarchy-v1", [
        SELF.replace("LEFT JOIN", "JOIN"), SELF.replace("m.id=u.manager_id", "m.id=u.id"),
        SELF.replace("m.id=u.manager_id", "u.id=m.manager_id"),
        SELF.replace("AS manager_email", "AS boss"),
        SELF.replace("m.email AS", "COALESCE(m.email,'NULL') AS"),
        SELF.replace("m.email AS", "COALESCE(m.email,'') AS"), SELF + " DESC",
        SELF.replace("ORDER BY u.id", "ORDER BY m.id,u.id"),
        SELF.replace("SELECT ", "SELECT DISTINCT ON (m.id) ", 1).replace("ORDER BY u.id", "ORDER BY m.id,u.id"),
        SELF.replace(" ORDER BY", " WHERE u.manager_id IS NOT NULL ORDER BY"),
        SELF.replace("m.email AS", "'a@example.com' AS"), SELF + " LIMIT 1",
    ])


@pytest.mark.parametrize("task_id,query", [
    ("sql.join.17", "SELECT o.id AS order_id,u.email FROM orders o CROSS JOIN users u"),
    ("sql.join.18", ANTI.replace("IS NULL", "IS NOT NULL")),
    ("sql.join.25", RIGHT.replace("RIGHT JOIN", "JOIN")),
    ("sql.join.20", SELF.replace("LEFT JOIN", "JOIN")),
])
def test_full_check_rejects_wrong_join_behavior_even_if_public_case_coincides(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] < 6
    if task_id == "sql.join.25":
        assert result["tests_passed"] == 2  # public products all sold; empty is also equal.
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,query", [
    ("sql.join.17", "SELECT * FROM (VALUES (10::bigint,'a@example.com'),(11::bigint,'a@example.com'),(12::bigint,'b@example.com'),(13::bigint,'b@example.com'),(14::bigint,'d@example.com')) v(order_id,email)"),
    ("sql.join.18", "SELECT 3::bigint AS id,'c@example.com' AS email"),
    ("sql.join.25", "SELECT * FROM (VALUES (100::bigint,10::bigint),(100::bigint,14::bigint),(101::bigint,10::bigint),(101::bigint,12::bigint),(102::bigint,13::bigint)) v(product_id,order_id) ORDER BY product_id,order_id"),
    ("sql.join.20", "SELECT * FROM (VALUES (1,'a@example.com',NULL::text),(2,'b@example.com','a@example.com'),(3,'c@example.com','a@example.com'),(4,'d@example.com','b@example.com')) v(id,email,manager_email) ORDER BY id".replace("SELECT *", "SELECT email,manager_email")),
])
def test_join_public_hardcoding_passes_only_one_of_six_cases(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] == 1
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id", ["sql.join.17", "sql.join.18", "sql.join.25", "sql.join.20"])
def test_join_check_keeps_explorer_unchanged_and_feedback_safe(manager, session, task_id):
    sid = session["session_id"]
    catalog = manager.catalog(sid, 1)
    before = manager.run(sid, 1, "SELECT * FROM users ORDER BY id")["rows"]
    assert grade(manager, task_id, task_for(task_id).reference_sql)["passed"]
    assert manager.catalog(sid, 1) == catalog
    assert manager.run(sid, 1, "SELECT * FROM users ORDER BY id")["rows"] == before
    error = grade(manager, task_id, "SELECT email::bigint AS order_id,email FROM users")
    assert not error["passed"] and error["feedback"][0]["sqlstate"] == "22P02"
    assert "@example" not in json.dumps(error)
    assert not {"reference_sql", "seed", "rows", "columns", "container_id"}.intersection(error)
    for query in ["UPDATE users SET manager_id=NULL", "CREATE TABLE bad(x int)", "SELECT 1; SELECT 2"]:
        assert grade(manager, task_id, query)["feedback"][0]["code"] == "policy"
    assert len(manager.backend.containers()) == 1


def test_join_truncation_and_streaming_join_timeout_never_pass(manager):
    large = "SELECT g AS order_id,u.email FROM (SELECT generate_series(1,501) g) s CROSS JOIN users u"
    assert grade(manager, "sql.join.17", large)["feedback"][0]["code"] == "result_limit"
    slow = "SELECT SUM(g) AS order_id,MIN(u.email) AS email FROM (SELECT generate_series(1,1000000000) g) s CROSS JOIN users u"
    result = grade(manager, "sql.join.17", slow)
    assert not result["passed"] and result["feedback"][0]["code"] == "timeout"
    assert not manager.backend.containers()


def test_full_outer_join_independent_values_preserves_both_unmatched_sides(manager, session):
    wanted = [["1", "local-only", None, None], ["2", "local-match", "2", "remote-match"], [None, None, "3", "remote-only"]]
    for join, rows in [("FULL OUTER", wanted), ("LEFT", wanted[:2]), ("RIGHT", wanted[1:]), ("INNER", wanted[1:2])]:
        output = manager.run(session["session_id"], 1, FULL.replace("FULL OUTER", join))
        assert output["error"] is None and not output["truncated"]
        assert output["rows"] == rows
        assert [c["pg_type"] for c in output["columns"]] == ["int4", "text", "int4", "text"]
    # FK-constrained shop-v1 has no orders without an owner, even with FULL JOIN.
    orphan = manager.run(session["session_id"], 1, "SELECT o.id FROM users u FULL JOIN orders o ON o.user_id=u.id WHERE u.id IS NULL")
    assert orphan["error"] is None and orphan["rows"] == []


FIXTURE_ROWS = {
    "sql.join.17": {
        "public-v1": [["10", "a@example.com"], ["11", "a@example.com"], ["12", "b@example.com"], ["13", "b@example.com"], ["14", "d@example.com"]],
        "empty-orders-v1": [],
        "repeated-owner-v1": [["501", "repeat@example.test"], ["18", "other@example.test"], ["42", "repeat@example.test"], ["2", "repeat@example.test"]],
        "crossed-ids-v1": [["99", "owner-seventeen@example.test"], ["2", "owner-ninety@example.test"], ["17", "owner-two@example.test"], ["250", "owner-seventeen@example.test"]],
        "bigint-v1": [["9007199254740995", "large-owner@example.test"]],
        "shuffled-v1": [["302", "owner9@example.test"], ["14", "owner4@example.test"], ["77", "owner81@example.test"], ["8", "owner9@example.test"], ["901", "owner81@example.test"], ["0", "owner9@example.test"]],
    },
    "sql.join.18": {
        "public-v1": [["3", "c@example.com"]],
        "mixed-v1": [["0", "mixed-zero@example.test"], ["901", "mixed-idle@example.test"], ["9007199254740993", "mixed-big@example.test"]],
        "all-have-v1": [], "all-without-v1": [["44", "idle44@example.test"], ["3", "idle3@example.test"], ["71", "idle71@example.test"]],
        "empty-v1": [], "bigint-v1": [["9007199254740993", "idle-huge@example.test"], ["0", "idle-zero@example.test"]],
    },
    "sql.join.25": {
        "public-v1": [["100", "10"], ["100", "14"], ["101", "10"], ["101", "12"], ["102", "13"]],
        "mixed-v1": [["0", "2"], ["401", None], ["700", "2"], ["700", "14"], ["700", "91"], ["9007199254740993", None]],
        "all-unsold-v1": [["7", None], ["51", None], ["80", None]], "empty-products-v1": [],
        "one-item-v1": [["13", None], ["99", "0"]],
        "shuffled-v1": [["0", "19"], ["8", "2"], ["51", None], ["9007199254740993", "19"], ["9007199254740993", "9007199254740995"]],
    },
    "sql.join.20": {
        "public-v1": [["a@example.com", None], ["b@example.com", "a@example.com"], ["c@example.com", "a@example.com"], ["d@example.com", "b@example.com"]],
        "hierarchy-v1": [["root-zero@example.test", None], ["early-employee@example.test", "mid@example.test"], ["mid@example.test", "z-root@example.test"], ["z-root@example.test", None], ["late-employee@example.test", "mid@example.test"], ["other-employee@example.test", "z-root@example.test"]],
        "one-v1": [["solo@example.test", None]], "empty-v1": [],
        "no-managers-v1": [["roots-a@example.test", None], ["roots-b@example.test", None], ["roots-c@example.test", None]],
        "shared-manager-v1": [["worker-k@example.test", "shared-chief@example.test"], ["worker-q@example.test", "shared-chief@example.test"], ["worker-a@example.test", "shared-chief@example.test"], ["worker-z@example.test", "shared-chief@example.test"], ["shared-chief@example.test", None]],
    },
}


@pytest.mark.parametrize("task_id", FIXTURE_ROWS)
def test_all_join_fixture_rows_are_independently_verified(manager, task_id):
    expected_types = {"sql.join.17": ["int8", "text"], "sql.join.18": ["int8", "text"], "sql.join.25": ["int8", "int8"], "sql.join.20": ["text", "text"]}
    for case_id, golden in FIXTURE_ROWS[task_id].items():
        with fixture(manager, task_id, case_id) as (handle, task):
            actual = run(manager, handle, task.reference_sql)
            assert actual["error"] is None and not actual["truncated"]
            assert [c["pg_type"] for c in actual["columns"]] == expected_types[task_id]
            if task.comparison == "ordered":
                assert actual["rows"] == golden, (task_id, case_id)
            else:
                assert Counter(map(tuple, actual["rows"])) == Counter(map(tuple, golden)), (task_id, case_id)
