from contextlib import contextmanager
import json
from pathlib import Path
import re
from uuid import uuid4

import pytest

from sql_runner.app.comparator import compare
from sql_runner.app.config import PYTHON
from sql_runner.app.grader import check
from sql_runner.app.grading_content import REGISTRY, load_task

LATEST = "SELECT id,created_at FROM orders ORDER BY created_at DESC,id DESC LIMIT 2"
COUNTRIES = "SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country"


def task_for(task_id):
    entry = REGISTRY[task_id]
    return load_task(task_id, entry.task_revision, entry.grader_revision)


def grade(manager, task_id, query):
    task = task_for(task_id)
    return check(manager, task_id, task.revision, task.grader_revision, query)


@contextmanager
def fixture(manager, task_id, case_id):
    task = task_for(task_id)
    case = next(case for case in task.cases if case.id == case_id)
    with manager.admission(), manager.registry:
        manager.require_capacity()
        handle = manager.backend.create("proof-" + uuid4().hex, 1, lifetime=60)
        manager.grading_handles.add(handle)
        try:
            if case.seed is not None:
                manager.backend.install_fixture(handle, case.seed)
            yield handle, task
        finally:
            manager.backend.remove(handle)
            manager.grading_handles.discard(handle)


def run(manager, handle, query):
    return manager.backend.execute(handle, "run", {"sql": query})


@pytest.mark.parametrize("task_id,query", [
    ("sql.basic.04", LATEST),
    ("sql.basic.04", "select o.id, o.created_at from lab.orders o order by 2 desc,1 desc fetch first 2 rows only"),
    ("sql.basic.05", COUNTRIES),
    ("sql.basic.05", "SELECT country FROM lab.users WHERE NOT (country IS NULL) GROUP BY country ORDER BY 1 ASC"),
])
def test_correct_and_equivalent_queries_pass_six_cases(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert result["passed"] and result["tests_passed"] == result["tests_total"] == 6
    assert not manager.backend.containers()


def test_date_only_order_is_deterministically_adversarial_not_accidental_heap_order(manager):
    query = "SELECT id,created_at FROM orders ORDER BY created_at DESC LIMIT 2"
    with fixture(manager, "sql.basic.04", "adversarial-ties-v1") as (handle, task):
        # Trusted test-only EXPLAIN, as the exact same OS/PG student role. Never
        # exposed through Run's AST policy or any new execution mode.
        code = ("import psycopg,json; c=psycopg.connect(host='/var/run/postgresql',dbname='lab',user='student',"
                "options='-c search_path=lab,pg_catalog -c default_transaction_read_only=on'); "
                "print(json.dumps(c.execute(" + repr("EXPLAIN (FORMAT JSON) " + query) + ").fetchone()[0][0]['Plan']))")
        response = manager.backend.client.containers.get(handle).exec_run([PYTHON, "-c", code], user="65532:65532")
        assert response.exit_code == 0
        plan = json.loads(response.output)
        assert plan["Node Type"] == "Limit"
        scan = plan["Plans"][0]
        assert scan["Node Type"] in {"Index Scan", "Index Only Scan"}
        assert scan["Index Name"] == "orders_adversarial_date_idx" and scan["Scan Direction"] == "Forward"
        expected = run(manager, handle, task.reference_sql)
        assert [r[0] for r in expected["rows"]] == ["21", "12"]
        for _ in range(3):
            actual = run(manager, handle, query)
            assert [r[0] for r in actual["rows"]] == ["11", "12"]
            assert compare(expected, actual, comparison="ordered", numeric_compatible=True) == "rows"


def test_wrong_order_limit_offset_columns_and_timestamp_types_fail(manager):
    queries = [
        "SELECT id,created_at FROM orders ORDER BY created_at ASC,id ASC LIMIT 2",
        "SELECT id,created_at FROM orders ORDER BY created_at DESC,id ASC LIMIT 2",
        "SELECT id,created_at FROM orders ORDER BY id DESC LIMIT 2",
        LATEST.replace(" LIMIT 2", ""), LATEST.replace("LIMIT 2", "LIMIT 1"), LATEST.replace("LIMIT 2", "LIMIT 3"),
        LATEST + " OFFSET 1",
        "SELECT created_at,id FROM orders ORDER BY created_at DESC,id DESC LIMIT 2",
        "SELECT id,created_at::date AS created_at FROM orders ORDER BY created_at DESC,id DESC LIMIT 2",
    ]
    with fixture(manager, "sql.basic.04", "adversarial-ties-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None
            assert compare(expected, actual, comparison="ordered", numeric_compatible=True) != "passed", query


def test_missing_distinct_null_exclusion_empty_string_or_wrong_order_fail(manager):
    queries = [
        "SELECT country FROM users WHERE country IS NOT NULL ORDER BY country",
        "SELECT DISTINCT country FROM users ORDER BY country",
        COUNTRIES + " DESC",
        "SELECT DISTINCT country FROM users WHERE country IS NOT NULL AND country <> '' ORDER BY country",
    ]
    with fixture(manager, "sql.basic.05", "mixed-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        assert expected["rows"] == [[""], ["AA"], ["NULL"], ["ZZ"]]
        for query in queries:
            actual = run(manager, handle, query)
            assert actual["error"] is None
            assert compare(expected, actual, comparison="ordered") != "passed", query
    # Replacing NULL with '' coincides with the correct result when '' already
    # exists. The NULL-only fixture separates those meanings deterministically.
    with fixture(manager, "sql.basic.05", "null-only-v1") as (handle, task):
        expected = run(manager, handle, task.reference_sql)
        actual = run(manager, handle, "SELECT DISTINCT COALESCE(country,'') AS country FROM users ORDER BY country")
        assert expected["rows"] == [] and actual["rows"] == [[""]]
        assert compare(expected, actual, comparison="ordered") == "rows"


@pytest.mark.parametrize("task_id,query", [
    ("sql.basic.04", "SELECT id,created_at FROM orders ORDER BY created_at DESC LIMIT 2"),
    ("sql.basic.05", "SELECT country FROM users WHERE country IS NOT NULL ORDER BY country"),
])
def test_full_check_rejects_missing_tie_key_or_missing_distinct(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] < 6
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,query", [
    ("sql.basic.04", "SELECT * FROM (VALUES (14::bigint,TIMESTAMPTZ '2026-02-05'),(13::bigint,TIMESTAMPTZ '2026-02-04')) v(id,created_at) ORDER BY created_at DESC,id DESC"),
    ("sql.basic.05", "SELECT country FROM (VALUES ('GE'),('KZ')) v(country) ORDER BY country"),
])
def test_hardcoded_baseline_passes_only_one_of_six_cases(manager, task_id, query):
    result = grade(manager, task_id, query)
    assert not result["passed"] and result["tests_passed"] == 1
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id", ["sql.basic.04", "sql.basic.05"])
def test_checks_preserve_explorer_hide_errors_and_keep_student_policy(manager, session, task_id):
    sid = session["session_id"]
    catalog = manager.catalog(sid, 1)
    before = manager.run(sid, 1, "SELECT * FROM orders ORDER BY id")["rows"]
    assert grade(manager, task_id, task_for(task_id).reference_sql)["passed"]
    assert manager.catalog(sid, 1) == catalog
    assert manager.run(sid, 1, "SELECT * FROM orders ORDER BY id")["rows"] == before
    query = "SELECT email::bigint AS country FROM users" if task_id == "sql.basic.05" else "SELECT email::bigint AS id,created_at FROM users"
    result = grade(manager, task_id, query)
    assert not result["passed"] and "@example" not in json.dumps(result)
    assert result["feedback"][0]["sqlstate"] == "22P02"
    for bad in ["DELETE FROM orders", "CREATE TABLE hacked(x int)", "SELECT 1; SELECT 2"]:
        assert grade(manager, task_id, bad)["feedback"][0]["code"] == "policy"
    assert len(manager.backend.containers()) == 1


def test_timeout_and_truncation_cannot_pass_ordered_tasks(manager):
    slow = "SELECT sum(g)::text AS country FROM (SELECT generate_series(1,1000000000) g) s"
    result = grade(manager, "sql.basic.05", slow)
    assert not result["passed"] and result["feedback"][0]["code"] == "timeout"
    large = "SELECT g AS id,TIMESTAMPTZ '2026-01-01' AS created_at FROM generate_series(1,501) g"
    result = grade(manager, "sql.basic.04", large)
    assert not result["passed"] and result["feedback"][0]["code"] == "result_limit"
    assert not manager.backend.containers()


def test_fixture_edge_cases_and_typed_timestamp_values(manager):
    expected = {
        "sql.basic.04": {
            "public-v1": ["14", "13"], "scrambled-v1": ["27", "5"], "adversarial-ties-v1": ["21", "12"],
            "single-v1": ["9007199254740993"], "empty-orders-v1": [], "instants-v1": ["41", "9"],
        },
        "sql.basic.05": {
            "public-v1": ["GE", "KZ"], "mixed-v1": ["", "AA", "NULL", "ZZ"], "all-same-v1": ["MX"],
            "null-only-v1": [], "changed-v1": ["CA", "DE", "US"], "empty-v1": [],
        },
    }
    for task_id, cases in expected.items():
        for case_id, values in cases.items():
            with fixture(manager, task_id, case_id) as (handle, task):
                result = run(manager, handle, task.reference_sql)
                assert result["error"] is None and not result["truncated"]
                assert [r[0] for r in result["rows"]] == values
                if task_id == "sql.basic.04":
                    assert result["columns"][1]["pg_type"] == "timestamptz"
                    if case_id in {"single-v1", "instants-v1"}:
                        assert all(r[1].endswith("00:00:00.123456Z") for r in result["rows"])
                if task_id == "sql.basic.05":
                    # PG17 stores database collation in pg_database, not the
                    # removed lc_collate GUC. This trusted metadata assertion
                    # uses the bootstrap owner; student catalog grants stay shut.
                    code = ("import psycopg,json; c=psycopg.connect(host='/var/run/postgresql',dbname='lab',user='postgres'); "
                            "print(json.dumps(c.execute(\"SELECT datcollate,datctype,datlocprovider FROM pg_catalog.pg_database WHERE datname='lab'\").fetchone()))")
                    response = manager.backend.client.containers.get(handle).exec_run([PYTHON, "-c", code], user="postgres")
                    assert response.exit_code == 0 and json.loads(response.output) == ["C", "C", "c"]


def test_all_new_lesson_sql_examples_match_the_described_public_results(manager, session):
    root = Path(__file__).resolve().parents[3] / "content/stage-10"
    # Expected values are independent of the query/reference result and mirror
    # each explanation in the manually curated lessons, in fenced-block order.
    expected = {
        "s10-order-by-limit-and-offset": [
            [["Python Book", "30.00"], ["SQL Book", "40.00"], ["Keyboard", "90.00"]],
            [["Keyboard", "90.00"], ["SQL Book", "40.00"], ["Python Book", "30.00"]],
            [["4", "GE"], ["1", "KZ"], ["2", "KZ"], ["3", None]],
            [["1", "a@example.com"], ["2", "b@example.com"]],
            [["3", "c@example.com"], ["4", "d@example.com"]],
            [["3", "c@example.com"], ["4", "d@example.com"]],
            [["Keyboard", "90.00"]],
            [["14", "2026-02-05T00:00:00Z"], ["13", "2026-02-04T00:00:00Z"]],
            [["SQL Book", "40.00"]],
        ],
        "s10-distinct": [
            [["books"], ["hardware"], ["books"]], [["books"], ["hardware"]],
            [["GE", True], ["KZ", True], [None, False]], [[""], ["NULL"], [None]],
            [["1"], ["2"]], [["books"], ["hardware"]],
            [["1", "a@example.com"], ["1", "a@example.com"], ["2", "b@example.com"], ["2", "b@example.com"], ["4", "d@example.com"]],
            [["1", "a@example.com"], ["2", "b@example.com"], ["4", "d@example.com"]],
            [["cancelled"], ["new"], ["paid"]], [["GE"], ["KZ"]],
            [["books", "30.00"], ["books", "40.00"], ["hardware", "90.00"]],
        ],
    }
    for slug, outputs in expected.items():
        queries = re.findall(r"```sql\n(.*?)```", (root / slug / "lesson.md").read_text(), re.S)
        assert len(queries) == len(outputs)
        for query, rows in zip(queries, outputs):
            result = manager.run(session["session_id"], 1, query)
            assert result["error"] is None, (slug, query, result["error"])
            assert not result["truncated"] and result["rows"] == rows, (slug, query, result["rows"], rows)
