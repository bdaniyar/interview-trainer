"""Real fixture, index, plan and equivalent-solution coverage."""
import os
from uuid import uuid4

import pytest

from index_lab.control import job, nodes, disposable
from index_lab.workloads import TASKS, PLAN_SQL
from sql_runner.app.config import PYTHON

pytestmark = pytest.mark.skipif(os.getenv("SQL_DOCKER_TESTS") != "1",
                                reason="Opt into disposable PostgreSQL Docker tests")
REFERENCE = {
    "pg.index.11.4.expression-v1": "CREATE INDEX email_folded ON users (lower(email))",
    "pg.index.11.6.composite-v1": "CREATE INDEX arrivals ON orders (hotel_id,arrival,id)",
    "pg.index.11.7.partial-v1": ("CREATE INDEX new_feed ON orders (created_at DESC, id DESC) "
                                "WHERE 'new'::text=status"),
    "pg.index.11.5.workload-v1": ("CREATE INDEX by_owner ON orders(user_id,created_at,id); "
                                 "CREATE INDEX by_recent ON orders(created_at,id) WHERE status='new'"),
    "pg.plan.11.8.analysis-v1": "EXPLAIN (ANALYZE, BUFFERS) " + PLAN_SQL,
    "pg.plan.11.15.range-v1": ("SELECT id, created_at FROM orders "
        "WHERE TIMESTAMP '2026-11-08 00:00:00' <= created_at "
        "AND created_at < TIMESTAMP '2026-11-09 00:00:00' ORDER BY created_at,id LIMIT 30"),
}
WRONG = {
    "pg.index.11.4.expression-v1": "CREATE INDEX email_regular ON users(email)",
    "pg.index.11.6.composite-v1": "CREATE INDEX swapped ON orders(arrival,hotel_id,id)",
    "pg.index.11.7.partial-v1": "CREATE INDEX all_feed ON orders(created_at,id)",
    "pg.index.11.5.workload-v1": ("CREATE INDEX owner_wrong ON orders(user_id,created_at,id) INCLUDE(total); "
                                 "CREATE INDEX by_recent ON orders(created_at,id) WHERE status='new'"),
    "pg.plan.11.8.analysis-v1": ("EXPLAIN (ANALYZE, BUFFERS) SELECT id, email FROM users WHERE id < 8 ORDER BY id"),
    "pg.plan.11.15.range-v1": ("SELECT id, created_at FROM orders "
        "WHERE TIMESTAMP '2026-11-08 00:00:00' < created_at "
        "AND created_at < TIMESTAMP '2026-11-09 00:00:00' ORDER BY created_at,id LIMIT 30"),
}


@pytest.fixture
def namespace():
    return "index-integration-" + uuid4().hex[:12]


@pytest.mark.parametrize("task_id", TASKS)
def test_all_real_hidden_fixtures_accept_correct_semantics(task_id, namespace):
    result = job(task_id, REFERENCE[task_id], namespace, grade=True)
    assert result["passed"] and result["tests_passed"] == result["tests_total"] == 6


@pytest.mark.parametrize("task_id", TASKS)
def test_wrong_design_or_query_is_rejected_with_real_postgresql(task_id, namespace):
    result = job(task_id, WRONG[task_id], namespace)
    assert not result["valid"], result


def test_public_run_has_buffers_real_rows_and_multiple_samples(namespace):
    task_id = "pg.plan.11.15.range-v1"
    result = job(task_id, REFERENCE[task_id], namespace)
    assert result["valid"]
    proof = result["runs"][0]
    assert len(proof["samples"]) == len(proof["baseline_samples"]) == 3
    assert proof["baseline_plan"] and proof["plan"]
    assert proof["plan"]["Actual Rows"] == proof["result"]["rows_returned"]
    assert "Shared Hit Blocks" in proof["plan"]
    assert any(s.get("Index Name") == "orders_day" for s in nodes(proof["controlled"]))


def test_student_role_is_read_only_even_without_ast_admission(namespace):
    probe = """import psycopg
with psycopg.connect(host='/var/run/postgresql', user='student', dbname='lab', autocommit=True) as conn:
    for command in ['CREATE INDEX x ON lab.orders(id)', "INSERT INTO lab.users VALUES(1,'a','b')"]:
        try:
            conn.execute(command)
        except psycopg.Error as exc:
            assert exc.sqlstate in ('42501', '25006')
        else:
            raise AssertionError('Untrusted role changed the database')
print('read-only')
"""
    with disposable(namespace) as (backend, handle):
        container = backend.client.containers.get(handle)
        assert container.attrs["HostConfig"]["NetworkMode"] == "none"
        assert not container.attrs["HostConfig"]["Binds"]
        result = container.exec_run([PYTHON, "-c", probe], user="65532:65532")
        assert result.exit_code == 0 and result.output == b"read-only\n", result.output


def test_inclusive_midnight_is_public_pass_but_hidden_failure(namespace):
    task_id = "pg.plan.11.15.range-v1"
    source = REFERENCE[task_id].replace("created_at < TIMESTAMP", "created_at <= TIMESTAMP")
    assert job(task_id, source, namespace)["valid"]
    result = job(task_id, source, namespace, grade=True)
    assert not result["passed"] and 1 <= result["tests_passed"] < 6


def test_plain_explain_reports_an_estimate_without_executing_query(namespace):
    task_id = "pg.plan.11.8.analysis-v1"
    estimated = job(task_id, "EXPLAIN " + PLAN_SQL, namespace)
    proof, = estimated["runs"]
    assert estimated["estimated"] and proof["estimated"]
    assert "Plan Rows" in proof["plan"] and "Actual Rows" not in proof["plan"]
    assert "result" not in proof


def test_query_must_keep_stable_order_on_tied_timestamps(namespace):
    task_id = "pg.plan.11.15.range-v1"
    source = REFERENCE[task_id].replace("ORDER BY created_at,id", "ORDER BY created_at")
    assert job(task_id, source, namespace)["valid"]
    result = job(task_id, source, namespace, grade=True)
    assert not result["passed"] and 1 <= result["tests_passed"] < 6


def test_student_query_error_only_exposes_sqlstate(namespace):
    task_id = "pg.plan.11.15.range-v1"
    preview = job(task_id, "SELECT id, created_at FROM orders WHERE id=1/0", namespace)
    assert not preview["valid"]
    assert preview["runs"] == [{"error": "postgres", "sqlstate": "22012"}]
