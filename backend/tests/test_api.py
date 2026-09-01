from __future__ import annotations

from backend.app import main as main_module


def test_course_catalog_contains_complete_backend_curriculum(client):
    response = client.get("/api/course")
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total"] == 359
    assert len(payload["modules"]) >= 30
    assert payload["modules"][0]["lessons"][0]["slug"] == "s00-diagnosticheskii-junior-python-backend-interview"


def test_full_interview_and_thematic_sets(client):
    full = client.get("/api/interview").json()
    assert full["active_set"] == "full-junior-backend"
    assert len(full["questions"]) == 25
    assert len(full["sets"]) == 20
    sql = client.get("/api/interview", params={"set_slug": "sql"}).json()
    assert len(sql["questions"]) == 30
    assert all(question["stage_slug"] == "stage-10" for question in sql["questions"])


def test_lesson_exposes_learn_flow_and_answer_levels(client):
    payload = client.get("/api/lessons/s02-dict").json()
    markdown = payload["markdown"]
    headings = [
        "## Теория",
        "### Что это",
        "### Как работает",
        "### Пример",
        "## Что нужно знать на Junior",
        "## Типичные ошибки",
        "## Практика",
        "## Вопросы с собеседований",
        "## Хорошие ответы",
        "## Критерии хорошего ответа",
    ]
    positions = [markdown.index(heading) for heading in headings]
    assert positions == sorted(positions)
    question = payload["interview"][0]
    assert question["short_answer"]
    assert question["junior_answer"]
    assert question["follow_up_question"]
    assert question["follow_up_answer"]


def test_user_files_survive_lesson_reload(client):
    files = {"main.py": "print('saved')\n", "service.py": "VALUE = 42\n"}
    saved = client.put("/api/lessons/is-vs-eq/files", json={"files": files})
    assert saved.status_code == 200
    lesson = client.get("/api/lessons/is-vs-eq").json()
    assert lesson["files"] == files


def test_open_lesson_marks_it_in_progress(client):
    response = client.post("/api/lessons/generators/open")
    assert response.json()["status"] == "in_progress"
    course = client.get("/api/course").json()
    generators = next(item for module in course["modules"] for item in module["lessons"] if item["slug"] == "generators")
    assert generators["status"] == "in_progress"


def test_successful_check_awards_xp_only_once(client, monkeypatch):
    async def fake_runner(_payload):
        return {
            "stdout": "3 passed\n",
            "stderr": "",
            "exit_code": 0,
            "timed_out": False,
            "duration_ms": 20,
            "tests": [
                {"name": "test_same_object", "status": "passed", "passed": True},
                {"name": "test_equal_distinct_objects", "status": "passed", "passed": True},
                {"name": "test_different_values", "status": "passed", "passed": True},
            ],
            "tests_passed": 3,
            "tests_total": 3,
        }

    monkeypatch.setattr(main_module, "execute_in_runner", fake_runner)
    payload = {"lesson_slug": "is-vs-eq", "files": {"main.py": "pass\n"}, "entrypoint": "main.py"}
    first = client.post("/api/check", json=payload).json()
    second = client.post("/api/check", json=payload).json()
    assert first["passed"] is True and first["xp_awarded"] == 20 and first["xp"] == 20
    assert second["passed"] is True and second["xp_awarded"] == 0 and second["xp"] == 20
    course = client.get("/api/course").json()
    assert course["summary"]["completed"] == 1


def test_theory_completion_is_idempotent(client):
    first = client.post("/api/progress/generators/theory", json={"completed": True}).json()
    second = client.post("/api/progress/generators/theory", json={"completed": True}).json()
    assert first["xp_awarded"] == 5
    assert second["xp_awarded"] == 0
    assert second["xp"] == 5
