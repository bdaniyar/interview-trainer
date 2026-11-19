"""Public scope and persistence for the private Transaction Lab controller."""
import asyncio
from hashlib import sha256
import os
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
import httpx
from pydantic import Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .content import content_repo
from .database import SessionLocal, get_db
from .sql_progress import completed, record, replay
from .sql_runner_client import SqlServiceError
from .sql_schemas import PublicFeedback, RequestModel, SqlCheck, SqlCheckResult, SqlGeneration, SqlRun

router = APIRouter(prefix="/api/transactions", tags=["Transaction Lab"])

TASKS = {
    "s11-mvcc-basics": ("increment", "pg.tx.11.11.stock-increment-v1",
        "-- Верните id и остаток после увеличения на 1.\nSELECT id, available FROM inventory WHERE id=1;"),
    "s10-data-modification": ("dml", "pg.write.10.25.status-v1",
        "-- Измените только заказ id=10 и верните id,status.\nSELECT id,status FROM orders WHERE id=10;"),
    "s11-booking-concurrency": ("booking", "pg.tx.11.17.booking-v1",
        "-- Забронируйте последнее место id=1. Используйте литерал 'REQUEST_KEY'.\nSELECT id,available FROM inventory;"),
}

SCENARIOS = {
    "read-committed": ("Read Committed", "Каждый оператор читает новый снимок. После COMMIT B сессия A видит новый остаток."),
    "repeatable-read": ("Repeatable Read", "Снимок A прежний, даже когда изменение B уже доступно новой транзакции."),
    "mvcc": ("MVCC", "Чтение A видит прежнюю версию строки, пока B сохраняет новую. COMMIT B не меняет снимок A."),
    "rollback-savepoint": ("SAVEPOINT и ROLLBACK", "Откат к точке сохраняет раннее изменение A, полный ROLLBACK отменяет и его."),
    "nowait": ("NOWAIT", "B сразу получает 55P03 на строке, заблокированной A. Для продолжения выполните ROLLBACK."),
    "skip-locked": ("SKIP LOCKED", "B пропускает занятую строку A. Это удобно для очереди, но не показывает все строки."),
    "blocking-update": ("Блокировка UPDATE", "PostgreSQL сообщает, что B ждёт A. После COMMIT A сессия B продолжает UPDATE."),
    "deadlock": ("Deadlock", "A и B берут строки в разном порядке. PostgreSQL прерывает одну операцию с 40P01. Повторяют транзакцию целиком."),
    "serializable": ("Serializable", "При несовместимых снимках один участник получает 40001. Повтор начинают с BEGIN."),
    "lost-update": ("Потерянное обновление", "Оба запроса вычисляют значение из старого остатка. Один инкремент теряется. Сравните с UPDATE available=available+1."),
    "exclusion": ("Пересечение интервалов", "После COMMIT A перекрывающийся интервал B отклоняется с 23P01."),
    "indexes": ("План запроса", "На маленькой таблице PostgreSQL может выбрать Seq Scan. План показывает выбор оптимизатора для этих данных."),
}

LESSONS = {
    "s10-data-modification": ("rollback-savepoint", "blocking-update"),
    "s11-constraints": ("exclusion",),
    "s11-composite-indexes-and-column-order": ("indexes",),
    "s11-explain-and-explain-analyze": ("indexes",),
    "s11-transactions-and-acid": ("rollback-savepoint", "lost-update"),
    "s11-isolation-levels": ("read-committed", "repeatable-read", "serializable"),
    "s11-mvcc-basics": ("mvcc", "read-committed"),
    "s11-locks": ("blocking-update", "nowait", "skip-locked"),
    "s11-deadlocks": ("deadlock",),
    "s11-booking-concurrency": ("blocking-update", "serializable", "exclusion"),
}

MESSAGES = {
    "busy": "Дождитесь завершения активной операции.",
    "workspace_active": "В другой вкладке открыта лаборатория. Закройте её или дождитесь истечения сессии.",
    "stale_session": "Поколение базы изменилось. Откройте новую лабораторию.",
    "session_closed": "Сессия закрыта. Запустите новую базу. Черновики сохранены в браузере.",
    "operation_gone": "Операция уже завершилась.",
    "policy": "Запрос не разрешён здесь. Используйте SELECT, ограниченный DML, команды транзакций или обычный EXPLAIN.",
    "runner_unavailable": "PostgreSQL Transaction Lab временно недоступен.",
}
GRADER = "transaction-v1"


def lesson_scope(slug):
    if slug not in LESSONS:
        raise SqlServiceError(404, "no_transaction_lab", "Для этого урока Transaction Lab недоступен.")
    lesson = content_repo.lesson(slug)
    task = TASKS.get(slug)
    return lesson, task


class Run(SqlRun):
    side: Literal["A", "B"]


class Cancel(SqlGeneration):
    side: Literal["A", "B"]
    operation: UUID


class ScenarioPayload(RequestModel):
    name: str = Field(max_length=80)


class TransactionService:
    def __init__(self, check_lock=None):
        self.url = os.getenv("TX_RUNNER_URL", "http://tx-runner:8003")
        self.client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(retries=0), trust_env=False)
        self.check_lock = check_lock or asyncio.Lock()

    async def call(self, path, payload, timeout=35):
        try:
            response = await self.client.post(self.url + path, json=payload,
                timeout=httpx.Timeout(timeout, connect=3))
            result = response.json()
        except (httpx.HTTPError, ValueError):
            raise SqlServiceError(503, "runner_unavailable", MESSAGES["runner_unavailable"]) from None
        if response.is_success and isinstance(result, dict):
            return result
        code = result.get("detail") if isinstance(result, dict) else None
        if path.startswith("/index/") and code == "policy":
            raise SqlServiceError(422, "policy",
                "Проверьте синтаксис упражнения. Здесь доступны только указанные определения индексов и SELECT с EXPLAIN для задач на планы.")
        if isinstance(code, str) and code in MESSAGES:
            raise SqlServiceError(response.status_code, code, MESSAGES[code])
        raise SqlServiceError(503, "runner_unavailable", MESSAGES["runner_unavailable"])

    async def check(self, slug, task_id, payload):
        lesson, spec = lesson_scope(slug)
        if not spec or spec[1] != task_id:
            raise SqlServiceError(404, "unknown_task", "Задание недоступно в этом уроке.")
        kind = spec[0]
        task = dict(id=task_id, lesson_id=lesson["id"], revision=1,
                    grader_revision=GRADER, dataset_checksum=TASK_CHECKSUMS[kind])
        return await self.grade_task(task, payload, "/grade", {"kind": kind, "sql": payload.sql},
            failed_message="Проверьте возвращённые строки, итог всех таблиц и границы транзакции.")

    async def grade_task(self, task, payload, endpoint, private_payload, *, failed_message):
        digest = sha256(payload.sql.encode()).hexdigest()
        with SessionLocal() as db:
            previous = replay(db, payload.request_id, task, digest)
        if previous:
            return previous
        if self.check_lock.locked():
            raise SqlServiceError(409, "busy", MESSAGES["busy"])
        async with self.check_lock:
            with SessionLocal() as db:
                previous = replay(db, payload.request_id, task, digest)
            if previous:
                return previous
            grade = await self.call(endpoint, private_payload, timeout=125)
            count = grade.get("tests_passed")
            if (grade.get("task_id"), grade.get("revision"), grade.get("tests_total")) != (
                    task["id"], task["revision"], 6) or type(count) is not int or not 0 <= count <= 6 or (
                    grade.get("passed") is not (count == 6)):
                raise SqlServiceError(503, "runner_unavailable", MESSAGES["runner_unavailable"])
            result = SqlCheckResult(request_id=payload.request_id, task_id=task["id"],
                task_revision=task["revision"], grader_revision=task["grader_revision"], passed=count == 6, tests_passed=count,
                tests_total=6, completed=False, feedback=[PublicFeedback(
                    code="passed" if count == 6 else "rows",
                    message="Все проверки пройдены." if count == 6 else
                    failed_message)])
            with SessionLocal() as db:
                try:
                    return record(db, task, digest, result)
                except IntegrityError:
                    db.rollback()
                    previous = replay(db, payload.request_id, task, digest)
                    if previous:
                        return previous
                    raise


# SHA-256 of the immutable Phase 8B fixture source. The image additionally
# verifies bootstrap / policy / executor compatibility before running any SQL.
TASK_CHECKSUMS = dict.fromkeys(("dml", "booking"), "69d3b0be8a1a25b7e3290aa5312293edb2bdeefed92c460810ffb1d114bacd8c")
TASK_CHECKSUMS["increment"] = "e2b9c5e11a2f6ec3e5758b32f569589b2ed7d8f5f00ba7a4968c797b766e3b24"


def service(request: Request):
    return request.app.state.transaction_lab


def scoped(slug):
    _, task = lesson_scope(slug)
    return {"slug": slug, "kind": task[0] if task else "practice"}


@router.get("/lessons/{slug}")
def manifest(slug: str, db: Session = Depends(get_db)):
    lesson, task = lesson_scope(slug)
    return dict(lesson_id=lesson["id"], task_id=task[1] if task else None,
                starter_sql=task[2] if task else "SELECT id, available FROM inventory ORDER BY id;",
                completed=completed(db, task[1]) if task else False,
                scenarios=[dict(id=name, title=SCENARIOS[name][0], expected=SCENARIOS[name][1])
                           for name in LESSONS[slug]])


@router.post("/lessons/{slug}/sessions", status_code=201)
async def create(slug: str, request: Request):
    return await service(request).call("/sessions", scoped(slug))


async def command(slug, sid, request, action, generation, **fields):
    return await service(request).call(f"/sessions/{sid}", scoped(slug) |
                                      dict(action=action, generation=generation) | fields)


@router.get("/lessons/{slug}/sessions/{sid}")
async def status(slug: str, sid: UUID, request: Request, generation: int = Query(ge=1),
                 after: int = Query(default=0, ge=0)):
    return await command(slug, sid, request, "status", generation, after=after)


@router.post("/lessons/{slug}/sessions/{sid}/run", status_code=202)
async def run(slug: str, sid: UUID, request: Request, payload: Run):
    return await command(slug, sid, request, "run", payload.generation, side=payload.side, sql=payload.sql)


@router.post("/lessons/{slug}/sessions/{sid}/cancel")
async def cancel(slug: str, sid: UUID, request: Request, payload: Cancel):
    return await command(slug, sid, request, "cancel", payload.generation,
                         side=payload.side, operation=str(payload.operation))


@router.post("/lessons/{slug}/sessions/{sid}/snapshot", status_code=202)
async def snapshot(slug: str, sid: UUID, request: Request, payload: SqlGeneration):
    return await command(slug, sid, request, "snapshot", payload.generation)


@router.post("/lessons/{slug}/sessions/{sid}/reset")
async def reset(slug: str, sid: UUID, request: Request, payload: SqlGeneration):
    return await command(slug, sid, request, "reset", payload.generation)


@router.delete("/lessons/{slug}/sessions/{sid}")
async def close(slug: str, sid: UUID, request: Request, generation: int = Query(ge=1)):
    return await command(slug, sid, request, "close", generation)


@router.post("/lessons/{slug}/tasks/{task_id}/check", response_model=SqlCheckResult)
async def check(slug: str, task_id: str, request: Request, payload: SqlCheck):
    return await service(request).check(slug, task_id, payload)


@router.post("/lessons/{slug}/scenario")
async def scenario(slug: str, request: Request, payload: ScenarioPayload):
    lesson_scope(slug)
    if payload.name not in LESSONS[slug]:
        raise SqlServiceError(404, "invalid_scenario", "Сценарий недоступен в этом уроке.")
    return await service(request).call("/scenario", {"name": payload.name})
