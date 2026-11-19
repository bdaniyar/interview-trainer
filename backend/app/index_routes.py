"""Public capability bindings and durable results for the advanced index tasks."""
from dataclasses import dataclass
from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import Field, field_validator
from sqlalchemy.orm import Session

from .content import content_repo
from .database import get_db
from .sql_progress import completed
from .sql_runner_client import SqlServiceError
from .sql_schemas import RequestModel, SqlCheck, SqlRun

router = APIRouter(prefix="/api/index-lab", tags=["PostgreSQL Index and Plan Lab"])
INDEX_FINGERPRINT = "b8fdc25cec9aea11599479730def342804fc90016482401fc36556dad76f6b71"


@dataclass(frozen=True)
class Spec:
    id: str
    title: str
    workload: Literal["index", "plan", "optimize"]
    prompt: str
    starter: str
    queries: tuple[str, ...]


LOWER = "SELECT id, email FROM users WHERE lower(email)='person7@example.test' ORDER BY id"
HOTEL = ("SELECT id, arrival FROM orders WHERE hotel_id=7 "
         "AND arrival >= DATE '2026-11-08' AND arrival < DATE '2026-11-11' "
         "ORDER BY arrival,id LIMIT 7")
NEW = "SELECT id, created_at FROM orders WHERE status='new' ORDER BY created_at DESC,id DESC LIMIT 6"
OWNER = "SELECT id, created_at FROM orders WHERE user_id=9 ORDER BY created_at DESC,id DESC LIMIT 6"
PLAN = ("SELECT o.id,u.email FROM orders o JOIN users u ON u.id=o.user_id "
        "WHERE o.hotel_id=7 AND o.status='new' ORDER BY o.id LIMIT 12")
DAY = ("SELECT id, created_at FROM orders WHERE created_at::date = DATE '2026-11-08' "
       "ORDER BY created_at,id LIMIT 30")

SPECS = {
    "s11-index-mental-model": Spec("pg.index.11.4.expression-v1",
        "Поиск email без учёта регистра", "index",
        "Задайте один B-tree для поиска по выражению lower(email). Проверьте реальные совпадения, включая несколько строк с одинаковым email после нормализации.",
        "CREATE INDEX email_lookup ON users (email);", (LOWER,)),
    "s11-composite-indexes-and-column-order": Spec("pg.index.11.6.composite-v1",
        "Лента бронирований одного отеля", "index",
        "Создайте один составной индекс, который найдёт записи одного отеля в диапазоне дат и поддержит ORDER BY arrival,id.",
        "CREATE INDEX arrivals ON orders (arrival);", (HOTEL,)),
    "s11-selectivity": Spec("pg.index.11.7.partial-v1",
        "Активная часть ленты", "index",
        "Индексируйте новые заказы для ленты. Архивные строки не должны входить в индекс. Сохраните порядок даты и id.",
        "CREATE INDEX recent ON orders (created_at);", (NEW,)),
    "s11-postgresql-b-tree": Spec("pg.index.11.5.workload-v1",
        "Две горячие выборки с ограниченным бюджетом", "index",
        "Выберите ровно два индекса для двух запросов. Один обслуживает ленту владельца, второй только новые заказы. Не добавляйте INCLUDE: выдача и так использует ключи, а индекс обслуживается на вставках.",
        "CREATE INDEX owner_lookup ON orders (user_id);", (OWNER, NEW)),
    "s11-explain-and-explain-analyze": Spec("pg.plan.11.8.analysis-v1",
        "Фактический план соединения", "plan",
        "Сначала снимите оценку через EXPLAIN. Для выполнения добавьте ANALYZE и BUFFERS. В плане сопоставьте оценку строк с фактом и числом проходов. Check сверяет результат соединения на разных наборах, SQLSTATE и наличие реальных счётчиков плана.",
        "EXPLAIN " + PLAN + ";", (PLAN,)),
    "s11-pagination": Spec("pg.plan.11.15.range-v1",
        "Страница по границам дня", "optimize",
        "Перепишите условие на индексируемый диапазон одного дня. Сохраните колонки, порядок и LIMIT. Проверьте моменты на границах дня. Check оценивает семантику и доступность индексного пути, а время показано для анализа.",
        DAY + ";", (DAY,)),
}


def binding(slug):
    spec = SPECS.get(slug)
    if spec is None:
        raise SqlServiceError(404, "unknown_task", "Для этого урока индексное упражнение недоступно.")
    return content_repo.lesson(slug), spec


class Preview(RequestModel):
    sql: str = Field(min_length=1, max_length=32768)

    @field_validator("sql")
    @classmethod
    def checked(cls, sql):
        return SqlRun.sql_budget(sql)


@router.get("/lessons/{slug}")
def manifest(slug: str, db: Session = Depends(get_db)):
    lesson, spec = binding(slug)
    return dict(lesson_id=lesson["id"], task_id=spec.id, workload=spec.workload,
                title=spec.title, prompt=spec.prompt, starter=spec.starter,
                queries=spec.queries, completed=completed(db, spec.id))


@router.post("/lessons/{slug}/run")
async def preview(slug: str, payload: Preview, request: Request):
    _, spec = binding(slug)
    return await request.app.state.transaction_lab.call("/index/run",
        {"task_id": spec.id, "sql": payload.sql}, timeout=50)


@router.post("/lessons/{slug}/check")
async def check(slug: str, payload: SqlCheck, request: Request):
    lesson, spec = binding(slug)
    task = dict(id=spec.id, lesson_id=lesson["id"], revision=1,
                grader_revision="index-v1", dataset_checksum=INDEX_FINGERPRINT)
    return await request.app.state.transaction_lab.grade_task(
        task, payload, "/index/check", {"task_id": spec.id, "sql": payload.sql},
        failed_message="Сверьте определение, точные строки и доступность нужного индексного пути.")
