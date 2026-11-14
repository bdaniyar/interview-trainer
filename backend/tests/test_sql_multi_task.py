from dataclasses import replace
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from backend.app import main
from backend.app.database import SessionLocal
from backend.app.models import SqlAttempt, SqlTaskProgress
from backend.app.sql_content import REGISTRY, build_registry, task_record
from backend.tests.test_sql_check import Grader, legacy_snapshot
from sql_runner.app.grading_content import load_task

SLUGS = ["s10-select-aliases-and-expressions", "s10-where-and-boolean-logic", "s10-null-and-three-valued-logic",
         "s10-order-by-limit-and-offset", "s10-distinct"]


def path(slug, task_id):
    return f"/api/sql/lessons/{slug}/tasks/{task_id}/check"


@pytest.fixture
def grader(client):
    grader = Grader()
    main.app.state.sql_checks.client = grader
    return grader


def test_backend_and_runner_registrations_agree_and_all_lessons_project_safe_manifests(client):
    for slug, spec in zip(SLUGS, REGISTRY.values()):
        manifest = client.get(f"/api/sql/lessons/{slug}").json()
        assert manifest["task_id"] == spec.task_id and manifest["can_check"] and not manifest["completed"]
        assert manifest["expected_columns"] == list(spec.expected_columns)
        assert client.get(f"/api/lessons/{slug}").json()["workspace_kind"] == "sql"
        assert not {"solution_sql", "reference_sql", "seed", "grader_revision", "rows_feedback"}.intersection(manifest)
        task = load_task(spec.task_id, spec.revision, spec.grader_revision)
        record = task_record(slug, spec.task_id)
        assert (task.dataset_id, task.dataset_checksum, task.expected_columns, task.comparison, len(task.cases)) == (
            record["dataset_id"], record["dataset_checksum"], tuple(record["expected_columns"]), record["comparison"], record["tests_total"])
    assert client.get("/api/sql/lessons/s10-aggregates").status_code == 404
    assert client.get("/api/lessons/s10-aggregates").json()["workspace_kind"] == "python"


def test_backend_registry_rejects_duplicate_tasks_and_lessons():
    a, b = list(REGISTRY.values())[:2]
    for duplicate in [replace(b, task_id=a.task_id), replace(b, lesson_id=a.lesson_id)]:
        with pytest.raises(ValueError, match="Duplicate"):
            build_registry([a, duplicate])


def test_independent_progress_idempotency_and_legacy_rows_across_all_five_tasks(client, grader):
    client.put("/api/lessons/is-vs-eq/files", json={"files": {"main.py": "KEEP = 123\n"}})
    client.post("/api/progress/generators/theory", json={"completed": True})
    with SessionLocal() as db:
        before = legacy_snapshot(db)
    solved = set()
    for slug, spec in zip(SLUGS, REGISTRY.values()):
        payload = {"request_id": str(uuid4()), "sql": "SELECT task_specific_query"}
        response = client.post(path(slug, spec.task_id), json=payload)
        assert response.status_code == 200 and response.json()["passed"]
        assert response.json()["tests_passed"] == spec.tests_total
        calls = grader.calls
        assert client.post(path(slug, spec.task_id), json=payload).json() == response.json()
        assert grader.calls == calls
        other = next(s for s in REGISTRY.values() if s.task_id != spec.task_id)
        other_slug = SLUGS[list(REGISTRY.values()).index(other)]
        assert client.post(path(other_slug, other.task_id), json=payload).status_code == 409
        solved.add(spec.task_id)
        for check_slug, check_spec in zip(SLUGS, REGISTRY.values()):
            assert client.get(f"/api/sql/lessons/{check_slug}").json()["completed"] == (check_spec.task_id in solved)
        grader.passed = False
        failed = client.post(path(slug, spec.task_id), json={"request_id": str(uuid4()), "sql": "SELECT wrong_query"}).json()
        assert not failed["passed"] and failed["completed"]
        grader.passed = True
    with SessionLocal() as db:
        assert legacy_snapshot(db) == before
        assert db.scalar(select(func.count()).select_from(SqlTaskProgress)) == 5
        assert db.scalar(select(func.count()).select_from(SqlAttempt)) == 10


def test_existing_first_three_task_attempt_and_progress_rows_are_preserved(client, grader):
    previous = list(REGISTRY.values())[:3]
    for slug, spec in zip(SLUGS[:3], previous):
        client.post(path(slug, spec.task_id), json={"request_id": str(uuid4()), "sql": "SELECT saved_task"})
    with SessionLocal() as db:
        attempt = db.execute(select(SqlAttempt.__table__).order_by(SqlAttempt.id)).all()
        progress = db.execute(select(SqlTaskProgress.__table__).order_by(SqlTaskProgress.id)).all()
    for slug, spec in zip(SLUGS[3:], list(REGISTRY.values())[3:]):
        assert client.post(path(slug, spec.task_id), json={"request_id": str(uuid4()), "sql": "SELECT new_task"}).json()["passed"]
    with SessionLocal() as db:
        ids = [spec.task_id for spec in previous]
        assert db.execute(select(SqlAttempt.__table__).where(SqlAttempt.task_id.in_(ids)).order_by(SqlAttempt.id)).all() == attempt
        assert db.execute(select(SqlTaskProgress.__table__).where(SqlTaskProgress.task_id.in_(ids)).order_by(SqlTaskProgress.id)).all() == progress


def test_cross_lesson_requests_fail_before_grader_and_feedback_is_task_aware(client, grader):
    specs = list(REGISTRY.values())
    for index, (slug, spec) in enumerate(zip(SLUGS, specs)):
        for other in specs:
            if other != spec:
                assert client.post(path(slug, other.task_id), json={"request_id": str(uuid4()), "sql": "SELECT 1"}).status_code == 404
        assert grader.calls == index * 2
        grader.passed, grader.code = False, "columns"
        columns = client.post(path(slug, spec.task_id), json={"request_id": str(uuid4()), "sql": "SELECT 1"}).json()
        assert ", ".join(spec.expected_columns) in columns["feedback"][0]["message"]
        if index:
            assert "user_id" not in columns["feedback"][0]["message"]
        grader.code = "rows"
        rows = client.post(path(slug, spec.task_id), json={"request_id": str(uuid4()), "sql": "SELECT 1"}).json()
        assert rows["feedback"][0]["message"] == spec.rows_feedback
    assert "NULL" in specs[2].rows_feedback and "фильтрации" in specs[1].rows_feedback
