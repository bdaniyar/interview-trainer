"""One admitted Check; task lookup and persistence stay server-owned."""
import asyncio
from hashlib import sha256

from .database import SessionLocal
from .sql_content import task_record
from .sql_progress import record, replay
from .sql_runner_client import SQLRunnerClient, SqlServiceError
from .sql_schemas import PublicFeedback, SqlCheckResult

MESSAGES = {
    "passed": "Запрос прошёл все проверки.",
    "policy": "Разрешён один read-only SELECT. Изменение данных, системные таблицы и административные функции запрещены.",
    "columns": "Проверьте названия и порядок столбцов: user_id, email. Для id нужен псевдоним user_id.",
    "types": "Типы столбцов не соответствуют условию. Сохраняйте исходные значения id и email.",
    "rows": "Результат не совпадает с условием на одном из наборов. Проверьте все строки, лишние строки и дубликаты.",
    "sql_error": "Запрос вызвал ошибку PostgreSQL на одном из наборов. Исправьте запрос и повторите Check.",
    "timeout": "Превышен лимит времени выполнения запроса.",
    "result_limit": "Результат превысил лимит строк или размера. Обрезанный результат не считается верным решением.",
}


class SQLChecks:
    def __init__(self, client=None, session_factory=SessionLocal):
        self.client = client or SQLRunnerClient()
        self.session_factory = session_factory
        self.lock = asyncio.Lock()

    async def check(self, slug, task_id, payload):
        task = task_record(slug, task_id)
        digest = sha256(payload.sql.encode("utf-8")).hexdigest()
        # Both reads close their transaction before the potentially long HTTP call.
        with self.session_factory() as db:
            previous = replay(db, payload.request_id, task, digest)
        if previous:
            return previous
        if self.lock.locked():
            raise SqlServiceError(409, "busy", "SQL Check уже выполняется. Дождитесь результата.")
        async with self.lock:
            with self.session_factory() as db:
                previous = replay(db, payload.request_id, task, digest)
            if previous:
                return previous
            grade = await self.client.check(task, payload.sql)
            if (grade.task_id, grade.task_revision, grade.grader_revision, grade.dataset_checksum, grade.tests_total) != (
                    task["id"], task["revision"], task["grader_revision"], task["dataset_checksum"], task["tests_total"]):
                raise SqlServiceError(503, "grader_protocol", "Некорректный ответ SQL Check. Повторите проверку.")
            result = SqlCheckResult(request_id=payload.request_id, task_id=task["id"], task_revision=task["revision"],
                grader_revision=task["grader_revision"], passed=grade.passed, tests_passed=grade.tests_passed,
                tests_total=grade.tests_total, completed=False,
                feedback=[PublicFeedback(code=f.code, message=MESSAGES[f.code], sqlstate=f.sqlstate) for f in grade.feedback])
            with self.session_factory() as db:
                return record(db, task, digest, result)
