"""Short additive SQLite transactions; no network call or XP changes here."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from .models import SqlAttempt, SqlTaskProgress
from .sql_runner_client import SqlServiceError
from .sql_schemas import SqlCheckResult
from .sql_sessions import LOCAL_PRINCIPAL


def completed(db, task_id):
    return db.scalar(select(SqlTaskProgress.id).where(
        SqlTaskProgress.owner == LOCAL_PRINCIPAL, SqlTaskProgress.task_id == task_id)) is not None


def replay(db, request_id, task, sql_hash):
    attempt = db.scalar(select(SqlAttempt).where(SqlAttempt.owner == LOCAL_PRINCIPAL, SqlAttempt.request_id == str(request_id)))
    if attempt is None:
        return None
    if (attempt.task_id, attempt.lesson_id, attempt.task_revision, attempt.grader_revision, attempt.sql_hash) != (
            task["id"], task["lesson_id"], task["revision"], task["grader_revision"], sql_hash):
        raise SqlServiceError(409, "request_conflict", "Этот request_id уже использован для другого SQL-запроса.")
    result = SqlCheckResult.model_validate_json(attempt.result_json)
    result.completed = completed(db, task["id"])
    return result


def record(db, task, sql_hash, result):
    if result.passed:
        now = datetime.utcnow()
        statement = insert(SqlTaskProgress).values(owner=LOCAL_PRINCIPAL, lesson_id=task["lesson_id"], task_id=task["id"],
            first_passed_at=now, last_passed_at=now, last_passed_revision=task["grader_revision"])
        db.execute(statement.on_conflict_do_update(index_elements=["owner", "task_id"], set_={
            "last_passed_at": now, "last_passed_revision": task["grader_revision"]}))
    result.completed = completed(db, task["id"])
    db.add(SqlAttempt(owner=LOCAL_PRINCIPAL, request_id=str(result.request_id), lesson_id=task["lesson_id"], task_id=task["id"],
        task_revision=task["revision"], grader_revision=task["grader_revision"], dataset_checksum=task["dataset_checksum"],
        sql_hash=sql_hash, passed=result.passed, tests_passed=result.tests_passed, tests_total=result.tests_total,
        result_json=result.model_dump_json()))
    db.commit()
    return result
