"""Server-owned capability manifest. Existing bank answers never enter this DTO."""
from fastapi import HTTPException

from .content import content_repo
from .sql_schemas import SqlLesson

GUIDED_LESSON_ID = "backend-interview.10.2.select-aliases-and-expressions"


def workspace_kind(metadata: dict) -> str:
    return "sql" if (metadata.get("id") == GUIDED_LESSON_ID
                     and metadata.get("content_status") == "complete") else "python"


def public_lesson(slug: str) -> SqlLesson:
    metadata, _ = content_repo.lesson_dir(slug)
    if workspace_kind(metadata) != "sql":
        raise HTTPException(404, "SQL Lab пока не подключён к этому уроку")
    return SqlLesson(
        lesson_id=metadata["id"], lesson_slug=metadata["slug"],
        starter_sql="SELECT id, email FROM users;\n",
        prompt="Выберите столбцы таблицы users. Попробуйте изменить их порядок и добавить псевдоним через AS, затем нажмите Run.",
    )
