"""Explicit lesson capabilities; only the public projection leaves the server."""
from dataclasses import dataclass
import json
from types import MappingProxyType

from fastapi import HTTPException

from .content import content_repo
from .sql_schemas import SqlLesson

DATASET_ID = "shop-v1"
DATASET_CHECKSUM = "a1de3973eb4a2febc818c026def43716109e7ffde6b0bc46721e11d1b2fa4b97"


@dataclass(frozen=True)
class Registration:
    lesson_id: str
    task_id: str
    revision: int
    grader_revision: str
    expected_columns: tuple[str, ...]
    tests_total: int
    prompt: str
    starter_sql: str
    rows_feedback: str
    column_hint: str = ""
    dataset_id: str = DATASET_ID
    dataset_checksum: str = DATASET_CHECKSUM
    comparison: str = "unordered"


def build_registry(entries):
    lessons, tasks = {}, set()
    for entry in entries:
        if entry.lesson_id in lessons or entry.task_id in tasks:
            raise ValueError("Duplicate SQL lesson/task registration")
        if entry.revision < 1 or not 1 <= entry.tests_total <= 16 or not entry.expected_columns:
            raise ValueError("Invalid SQL task registration")
        lessons[entry.lesson_id] = entry
        tasks.add(entry.task_id)
    return MappingProxyType(lessons)


REGISTRY = build_registry((
    Registration("backend-interview.10.2.select-aliases-and-expressions", "sql.guided.10.2.projection.v1", 1,
        "projection-v1", ("user_id", "email"), 4,
        "Выведите id и email всех пользователей из users. Назовите столбец id псевдонимом user_id. Результат должен содержать только столбцы user_id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email FROM users;\n",
        "Результат не совпадает с условием на одном из наборов. Проверьте все строки, лишние строки и дубликаты.",
        "Для id нужен псевдоним user_id."),
    Registration("backend-interview.10.3.where-and-boolean-logic", "sql.basic.01", 1,
        "active-users-v1", ("id", "email"), 5,
        "Выведите id и email пользователей из users, у которых active = true. Только столбцы id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email\nFROM users;\n",
        "Проверьте условие фильтрации: нужны все активные пользователи, без лишних строк и дубликатов."),
    Registration("backend-interview.10.4.null-and-three-valued-logic", "sql.basic.03", 1,
        "null-country-v1", ("id", "email"), 5,
        "Выведите id и email пользователей из users, для которых country неизвестна (NULL). Только столбцы id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email\nFROM users;\n",
        "Проверьте работу с неизвестными значениями. SQL NULL отличается от пустой строки и обычного значения; учтите все нужные строки и дубликаты."),
    Registration("backend-interview.10.5.order-by-limit-and-offset", "sql.basic.04", 1,
        "latest-orders-v1", ("id", "created_at"), 6,
        "Верните два последних заказа по created_at. При одинаковой дате заказ с большим id должен идти первым. Только столбцы id и created_at в этом порядке. Если заказов меньше двух, верните все имеющиеся.",
        "SELECT id, created_at\nFROM orders;\n",
        "Проверьте направление сортировки, порядок заказов при одинаковой дате и ограничение количества строк.",
        comparison="ordered"),
    Registration("backend-interview.10.6.distinct", "sql.basic.05", 1,
        "distinct-countries-v1", ("country",), 6,
        "Выведите уникальные значения country из users. Исключите SQL NULL и отсортируйте страны по возрастанию. Только столбец country. Пустая строка является значением и должна остаться, если встречается в данных.",
        "SELECT country\nFROM users;\n",
        "Проверьте повторы, исключение SQL NULL и сортировку по возрастанию. Пустая строка не равна NULL.",
        comparison="ordered"),
    Registration("backend-interview.10.7.aggregates", "sql.aggregation.09", 1,
        "count-orders-v1", ("orders_count",), 6,
        "Посчитайте общее количество заказов в orders. Верните одну строку с одним столбцом orders_count. Если заказов нет, результат должен содержать число 0.",
        "SELECT id, status\nFROM orders;\n",
        "Проверьте источник подсчёта и число строк результата: нужна одна строка с количеством всех заказов, включая 0 для пустой таблицы.",
        comparison="ordered"),
    Registration("backend-interview.10.8.group-by", "sql.aggregation.10", 1,
        "orders-by-status-v1", ("status", "count"), 6,
        "Посчитайте количество заказов для каждого status. Верните status и count в этом порядке, отсортировав строки по status по возрастанию.",
        "SELECT status\nFROM orders;\n",
        "Проверьте состав групп, количество заказов в каждой группе и сортировку по status. Нужна одна строка на каждый имеющийся статус.",
        comparison="ordered"),
    Registration("backend-interview.10.9.having", "sql.aggregation.13", 1,
        "users-with-two-orders-v1", ("user_id", "count"), 6,
        "Найдите пользователей, у которых минимум два заказа. Верните user_id и количество заказов под названием count. Отсортируйте результат по user_id по возрастанию.",
        "SELECT user_id\nFROM orders;\n",
        "Проверьте количество заказов каждого пользователя и границу «минимум два»: два и больше подходят, один — нет. Учтите точный count и порядок user_id.",
        comparison="ordered"),
))


def workspace_kind(metadata: dict) -> str:
    return "sql" if metadata.get("id") in REGISTRY and metadata.get("content_status") == "complete" else "python"


def task_record(slug: str, task_id: str) -> dict:
    metadata, _ = content_repo.lesson_dir(slug)
    spec = REGISTRY.get(metadata["id"])
    if workspace_kind(metadata) != "sql" or spec.task_id != task_id:
        raise HTTPException(404, "SQL-задание не подключено к этому уроку")
    bank = json.loads((content_repo.root / "practice_banks.json").read_text(encoding="utf-8"))
    matches = [item for item in bank["sql"] if item["id"] == spec.task_id]
    if len(matches) != 1 or (matches[0].get("expected_columns"), matches[0].get("comparison")) != (
            list(spec.expected_columns), spec.comparison):
        raise HTTPException(503, "Конфигурация SQL-задания временно недоступна")
    record = matches[0]
    # basic.01's legacy lesson_number says 10.2; this explicit capability mapping
    # enables it in 10.3 without rewriting its historical bank record.
    fields = dict(id=spec.task_id, lesson_id=spec.lesson_id, revision=spec.revision,
        grader_revision=spec.grader_revision, dataset_id=spec.dataset_id, dataset_checksum=spec.dataset_checksum,
        expected_columns=list(spec.expected_columns), comparison=spec.comparison, tests_total=spec.tests_total)
    if any(key in record and record[key] != value for key, value in fields.items()):
        raise HTTPException(503, "Конфигурация SQL-задания временно недоступна")
    return record | fields | dict(prompt=spec.prompt, starter_sql=spec.starter_sql,
                                 rows_feedback=spec.rows_feedback, column_hint=spec.column_hint)


def public_lesson(slug: str) -> SqlLesson:
    metadata, _ = content_repo.lesson_dir(slug)
    if workspace_kind(metadata) != "sql":
        raise HTTPException(404, "SQL Lab пока не подключён к этому уроку")
    task = task_record(slug, REGISTRY[metadata["id"]].task_id)
    return SqlLesson(lesson_id=metadata["id"], lesson_slug=metadata["slug"], dataset_id=task["dataset_id"],
        task_id=task["id"], task_revision=task["revision"], can_check=True,
        starter_sql=task["starter_sql"], prompt=task["prompt"], expected_columns=task["expected_columns"])
