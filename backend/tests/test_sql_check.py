import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Event
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from backend.app import main
from backend.app.database import Base, SessionLocal
from backend.app.models import Attempt, CodeFile, InterviewProgress, LessonProgress, SqlAttempt, SqlTaskProgress, UserState
from backend.app.sql_content import TASK_ID, task_record
from backend.app.sql_runner_client import SQLRunnerClient, SqlServiceError
from backend.app.sql_schemas import RunnerGrade, SqlCheckResult

SLUG = "s10-select-aliases-and-expressions"
PATH = f"/api/sql/lessons/{SLUG}/tasks/{TASK_ID}/check"
QUERY = "SELECT id AS user_id,email FROM users"
LEGACY = [UserState.__table__, LessonProgress.__table__, CodeFile.__table__, Attempt.__table__, InterviewProgress.__table__]


class Grader:
    def __init__(self):
        self.calls = 0
        self.passed = True
        self.code = "rows"
        self.failure = False
        self.block = False
        self.started, self.release = Event(), Event()

    async def check(self, task, query):
        self.calls += 1
        if self.block:
            self.started.set()
            while not self.release.is_set():
                await asyncio.sleep(0.01)
        if self.failure:
            raise SqlServiceError(503, "grading_unavailable", "Проверка временно недоступна")
        return RunnerGrade(task_id=task["id"], task_revision=task["revision"], grader_revision=task["grader_revision"],
            dataset_checksum=task["dataset_checksum"], passed=self.passed, tests_total=4, tests_passed=4 if self.passed else 1,
            feedback=[{"code": "passed" if self.passed else self.code, "sqlstate": None}])


@pytest.fixture
def grader(client):
    fake = Grader()
    main.app.state.sql_checks.client = fake
    yield fake
    fake.release.set()


def check(client, query=QUERY, request_id=None):
    return client.post(PATH, json={"sql": query, "request_id": request_id or str(uuid4())})


def legacy_snapshot(db):
    return {table.name: db.execute(select(table).order_by(*table.primary_key.columns)).all() for table in LEGACY}


def test_pass_then_fail_is_sticky_and_preserves_all_python_state_and_xp(client, grader):
    client.put("/api/lessons/is-vs-eq/files", json={"files": {"main.py": "PRIVATE_SAVED = 42\n", "extra.py": "EXTRA = True"}})
    client.post("/api/progress/generators/theory", json={"completed": True})
    client.get(f"/api/lessons/{SLUG}")
    with SessionLocal() as db:
        before = legacy_snapshot(db)
    passed = check(client).json()
    assert passed["passed"] and passed["completed"] and passed["tests_passed"] == passed["tests_total"] == 4
    with SessionLocal() as db:
        first_pass = db.scalar(select(SqlTaskProgress.first_passed_at))
    grader.passed = False
    failed = check(client, "SELECT id,email FROM users").json()
    assert not failed["passed"] and failed["completed"]
    assert client.get(f"/api/sql/lessons/{SLUG}").json()["completed"] is True
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(SqlAttempt)) == 2
        assert db.scalar(select(func.count()).select_from(SqlTaskProgress)) == 1
        assert db.scalar(select(SqlTaskProgress.first_passed_at)) == first_pass
        assert legacy_snapshot(db) == before


def test_request_id_is_idempotent_and_cannot_be_reused_for_another_query(client, grader):
    token = str(uuid4())
    assert check(client, request_id=token).status_code == 200
    assert check(client, request_id=token).json()["passed"]
    assert grader.calls == 1
    assert check(client, "SELECT 1", token).status_code == 409
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(SqlAttempt)) == 1


def test_failed_attempt_replay_observes_later_completion_without_grading_again(client, grader):
    grader.passed = False
    token = str(uuid4())
    assert check(client, request_id=token).json()["completed"] is False
    grader.passed = True
    assert check(client).json()["completed"] is True
    replay = check(client, request_id=token).json()
    assert replay["passed"] is False and replay["completed"] is True and grader.calls == 2


def test_check_is_independent_of_editor_session_and_client_cannot_choose_rules(client, grader):
    assert not main.app.state.sql_sessions.bindings
    assert check(client).json()["passed"]
    assert not main.app.state.sql_sessions.bindings
    for extra in ["hidden_seed", "reference_sql", "image", "owner", "expected_rows", "passed", "xp_awarded", "grader_revision", "session_id"]:
        response = client.post(PATH, json={"sql": QUERY, "request_id": str(uuid4()), extra: "injected"})
        assert response.status_code == 422
    for path in [PATH.replace(TASK_ID, "sql.basic.01"), PATH.replace(SLUG, "is-vs-eq")]:
        assert client.post(path, json={"sql": QUERY, "request_id": str(uuid4())}).status_code == 404
    assert grader.calls == 1


def test_busy_timeout_and_infrastructure_failure_never_create_false_success(client, grader):
    grader.block = True
    with ThreadPoolExecutor(1) as pool:
        running = pool.submit(check, client)
        assert grader.started.wait(2)
        try:
            assert check(client).status_code == 409
        finally:
            grader.release.set()
        assert running.result(timeout=3).json()["passed"]
    grader.block = False
    grader.passed, grader.code = False, "timeout"
    response = check(client).json()
    assert not response["passed"] and response["completed"] and response["feedback"][0]["code"] == "timeout"
    grader.failure = True
    assert check(client).status_code == 503
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(SqlAttempt)) == 2
        assert db.scalar(select(func.count()).select_from(SqlTaskProgress)) == 1


def test_only_safe_feedback_codes_cross_runner_and_public_api(client, grader):
    task = task_record(SLUG, TASK_ID)
    response = dict(task_id=TASK_ID, task_revision=1, grader_revision="projection-v1", dataset_checksum=task["dataset_checksum"],
        passed=False, tests_passed=0, tests_total=4, reference_sql="PRIVATE REFERENCE", hidden_rows=[["PRIVATE ROW"]],
        feedback=[{"code": "sql_error", "sqlstate": "22P02", "message": "PRIVATE HIDDEN VALUE", "detail": "PRIVATE SEED"}])
    main.app.state.sql_checks.client = SQLRunnerClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=response)))
    public = check(client)
    assert public.status_code == 200 and "PRIVATE" not in public.text
    assert public.json()["feedback"][0]["sqlstate"] == "22P02"
    response["task_id"] = "foreign-task"
    assert check(client).status_code == 503
    response["task_id"] = TASK_ID
    response["passed"] = True  # incoherent counts/feedback, not an authoritative pass
    assert check(client).status_code == 503


def test_additive_upgrade_preserves_an_existing_legacy_sqlite_database(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    Base.metadata.create_all(engine, tables=LEGACY)
    with Session(engine) as db:
        db.add_all([UserState(id=1, xp=777, last_opened_lesson="is-vs-eq", theme="light"),
            LessonProgress(lesson_slug="is-vs-eq", task_completed=True, theory_completed=True, status="completed"),
            CodeFile(lesson_slug="is-vs-eq", path="extra.py", content="SAVED = 777"),
            Attempt(lesson_slug="is-vs-eq", kind="check", passed=True, stdout="old output"),
            InterviewProgress(question_id="old-question", answer="old answer")])
        db.commit()
        before = legacy_snapshot(db)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        from backend.app.sql_progress import record
        task = task_record(SLUG, TASK_ID)
        output = SqlCheckResult(request_id=uuid4(), task_id=TASK_ID, task_revision=1, grader_revision="projection-v1", passed=True,
            tests_passed=4, tests_total=4, completed=False, feedback=[{"code": "passed", "message": "ok"}])
        record(db, task, "0" * 64, output)
        assert legacy_snapshot(db) == before
        assert db.scalar(select(SqlTaskProgress.task_id)) == TASK_ID
    engine.dispose()
