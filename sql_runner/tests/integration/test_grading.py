from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from time import sleep

from fastapi.testclient import TestClient
import pytest

from sql_runner.app.grader import check
from sql_runner.app.grading_content import GRADER_REVISION, TASK_ID, load_task
from sql_runner.app.lifecycle import SessionError
from sql_runner.app.main import create_app

CORRECT = "SELECT id AS user_id,email FROM users"
SLOW = "SELECT sum(g) AS user_id, 'x' AS email FROM (SELECT generate_series(1,1000000000) AS g) s"


def grade(manager, query):
    return check(manager, TASK_ID, 1, GRADER_REVISION, query)


def test_correct_projection_and_reverse_order_pass_without_mutating_explorer(manager, session):
    sid = session["session_id"]
    before = manager.run(sid, 1, "SELECT * FROM users ORDER BY id")
    catalog = manager.catalog(sid, 1)
    assert grade(manager, CORRECT)["tests_passed"] == 4
    assert grade(manager, CORRECT + " ORDER BY id DESC")["passed"]
    assert grade(manager, "SELECT id::numeric AS user_id,email FROM users")["passed"]
    after = manager.run(sid, 1, "SELECT * FROM users ORDER BY id")
    assert before["rows"] == after["rows"] and manager.catalog(sid, 1) == catalog
    assert len(manager.backend.containers()) == 1
    box = manager.backend.client.containers.get(manager.sessions[sid].handle)
    assert box.exec_run(["test", "-e", "/opt/runner/sql_runner/grading"], user="65532:65532").exit_code == 1


@pytest.mark.parametrize("query", [
    "SELECT id,email FROM users",
    "SELECT email,id AS user_id FROM users",
    CORRECT + " LIMIT 1",
    CORRECT + " UNION ALL " + CORRECT,
    "SELECT id::float8 AS user_id,email FROM users",
    "SELECT 1 AS user_id,'a@example.com' AS email",
])
def test_wrong_alias_columns_missing_extra_duplicate_and_hardcoded_rows_fail(manager, query):
    output = grade(manager, query)
    assert not output["passed"] and output["tests_passed"] < 4
    assert not manager.backend.containers()


def test_all_public_rows_hardcoded_pass_only_the_public_case(manager):
    query = """SELECT * FROM (VALUES
        (1::bigint,'a@example.com'), (2::bigint,'b@example.com'),
        (3::bigint,'c@example.com'), (4::bigint,'d@example.com')) t(user_id,email)"""
    output = grade(manager, query)
    assert output["tests_passed"] == 1 and not output["passed"]
    assert not manager.backend.containers()


def test_hidden_values_are_not_exposed_by_postgres_cast_errors(manager):
    output = grade(manager, "SELECT id AS user_id,email::bigint AS email FROM users")
    assert not output["passed"]
    wire = json.dumps(output)
    for secret in ["Renée", "Mixed.Case", "extra-nine", "a@example.com", "reference_sql", "seed_file"]:
        assert secret not in wire
    assert any(item["sqlstate"] == "22P02" for item in output["feedback"])


@pytest.mark.parametrize("query", ["DELETE FROM users", "SELECT 1; SELECT 2", "WITH x AS (DELETE FROM users RETURNING *) SELECT * FROM x"])
def test_grading_reuses_select_policy_without_creating_containers(manager, query):
    output = grade(manager, query)
    assert not output["passed"] and output["feedback"][0]["code"] == "policy"
    assert not manager.backend.containers()


def test_truncation_statement_timeout_and_capacity_cannot_pass(manager):
    output = grade(manager, "SELECT g AS user_id,'x' AS email FROM generate_series(1,501) g")
    assert not output["passed"] and output["feedback"][0]["code"] == "result_limit"
    output = grade(manager, SLOW)
    assert not output["passed"] and output["feedback"][0]["code"] == "timeout"
    assert not manager.backend.containers()
    manager.create(); manager.create()
    with pytest.raises(SessionError) as error:
        grade(manager, CORRECT)
    assert error.value.status == 429 and len(manager.backend.containers()) == 2


def test_actual_crash_during_grading_is_not_student_success_and_cleans_only_grade_case(manager, session, monkeypatch):
    execute = manager.backend.execute

    def crash(handle, operation, payload):
        if payload["sql"] == load_task().reference_sql:
            return execute(handle, operation, payload)
        with ThreadPoolExecutor(1) as pool:
            running = pool.submit(execute, handle, operation, payload)
            sleep(0.3)
            manager.backend.client.containers.get(handle).kill()
            return running.result(timeout=8)

    monkeypatch.setattr(manager.backend, "execute", crash)
    with pytest.raises(SessionError) as error:
        grade(manager, SLOW)
    assert error.value.status == 503
    assert len(manager.backend.containers()) == 1
    monkeypatch.setattr(manager.backend, "execute", execute)
    assert manager.run(session["session_id"], 1, "SELECT count(*) FROM users")["rows"] == [["4"]]


def test_external_student_deadline_destroys_each_disposable_case(manager, monkeypatch):
    execute = manager.backend.execute

    def deadline(handle, operation, payload):
        if payload["sql"] == load_task().reference_sql:
            return execute(handle, operation, payload)
        original = manager.backend.settings
        manager.backend.settings = replace(original, query_seconds=0.05)
        try:
            return execute(handle, operation, payload)
        finally:
            manager.backend.settings = original

    monkeypatch.setattr(manager.backend, "execute", deadline)
    output = grade(manager, SLOW)
    assert not output["passed"] and output["feedback"][0]["code"] == "timeout"
    assert not manager.backend.containers()


def test_internal_check_contract_has_no_client_selected_fixtures(settings):
    with TestClient(create_app(settings)) as api:
        payload = dict(task_id=TASK_ID, task_revision=1, grader_revision=GRADER_REVISION, sql=CORRECT)
        response = api.post("/v1/check", json=payload)
        assert response.status_code == 200 and response.json()["passed"]
        for field in ("seed", "reference_sql", "expected_rows", "session_id"):
            assert api.post("/v1/check", json=payload | {field: "injected"}).status_code == 422
        assert api.post("/v1/check", json=payload | {"task_id": "../../etc/passwd"}).status_code == 404
