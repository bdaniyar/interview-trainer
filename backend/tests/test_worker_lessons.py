"""New capabilities must keep the learner's earlier files, theory and XP."""

import pytest
from sqlalchemy import select
from backend.app.database import SessionLocal
from backend.app.models import LessonProgress

SLUGS = [
    "s20-fastapi-backgroundtasks",
    "s20-retry-and-backoff",
    "s20-idempotency",
    "s20-periodic-tasks",
    "s20-delivery-semantics",
]


@pytest.mark.parametrize("slug", SLUGS)
def test_new_worker_task_preserves_existing_draft_and_theory(client, slug):
    files = {
        "main.py": "# My earlier study notes\nprint('keep')\n",
        "notes.py": "VALUE = 42\n",
    }
    assert (
        client.put(f"/api/lessons/{slug}/files", json={"files": files}).status_code
        == 200
    )
    theory = client.post(
        f"/api/progress/{slug}/theory", json={"completed": True}
    ).json()
    # Simulate completion saved before this legacy lesson gained a coding task.
    with SessionLocal() as session:
        row = session.scalar(
            select(LessonProgress).where(LessonProgress.lesson_slug == slug)
        )
        row.status = "completed"
        session.commit()
    before = client.get("/api/course").json()["summary"]["xp"]
    lesson = client.get(f"/api/lessons/{slug}").json()
    assert (
        lesson["workspace_kind"] == "python"
        and lesson["has_task"]
        and lesson["has_solution"]
    )
    assert lesson["files"] == files and lesson["progress"]["theory_completed"]
    assert not lesson["progress"]["task_completed"]
    assert lesson["progress"]["status"] == "completed"
    assert "tests" not in lesson and "hidden_tests" not in lesson
    assert (
        client.post(f"/api/progress/{slug}/theory", json={"completed": True}).json()[
            "xp_awarded"
        ]
        == 0
    )
    assert client.get("/api/course").json()["summary"]["xp"] == before == theory["xp"]
