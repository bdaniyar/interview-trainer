"""Server-owned capability manifest. Existing bank answers never enter this DTO."""
import json
from fastapi import HTTPException

from .content import content_repo
from .sql_schemas import SqlLesson

GUIDED_LESSON_ID = "backend-interview.10.2.select-aliases-and-expressions"
TASK_ID = "sql.guided.10.2.projection.v1"


def workspace_kind(metadata: dict) -> str:
    return "sql" if (metadata.get("id") == GUIDED_LESSON_ID
                     and metadata.get("content_status") == "complete") else "python"


def public_lesson(slug: str) -> SqlLesson:
    metadata, _ = content_repo.lesson_dir(slug)
    if workspace_kind(metadata) != "sql":
        raise HTTPException(404, "SQL Lab пока не подключён к этому уроку")
    task = task_record(slug, TASK_ID)
    return SqlLesson(
        lesson_id=metadata["id"], lesson_slug=metadata["slug"],
        task_id=task["id"], task_revision=task["revision"], can_check=True,
        starter_sql=task["starter_sql"], prompt=task["prompt"], expected_columns=task["expected_columns"],
    )


def task_record(slug: str, task_id: str) -> dict:
    metadata, _ = content_repo.lesson_dir(slug)
    if workspace_kind(metadata) != "sql" or task_id != TASK_ID:
        raise HTTPException(404, "SQL-задание не подключено к этому уроку")
    bank = json.loads((content_repo.root / "practice_banks.json").read_text(encoding="utf-8"))
    record = next((item for item in bank["sql"] if item["id"] == TASK_ID), None)
    if not record or (record.get("lesson_id"), record.get("dataset_id"), record.get("kind"), record.get("revision"), record.get("grader_revision"), record.get("tests_total")) != (
            GUIDED_LESSON_ID, "shop-v1", "graded_select", 1, "projection-v1", 4):
        raise HTTPException(503, "Конфигурация SQL-задания временно недоступна")
    return record
