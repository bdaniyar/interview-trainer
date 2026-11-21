from __future__ import annotations

from backend.app import main as main_module


def test_course_catalog_contains_complete_backend_curriculum(client):
    response = client.get("/api/course")
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total"] == 370
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


def test_ai_catalog_and_guided_completion_preserve_backend_progress(client):
    slug = "ai01-ai-roles-and-boundaries"
    backend_slug = "generators"
    files = {"main.py": "print('backend draft')", "notes.py": "X = 4"}
    client.put(f"/api/lessons/{backend_slug}/files", json={"files": files}).raise_for_status()
    client.post(f"/api/lessons/{backend_slug}/open").raise_for_status()
    client.post(f"/api/progress/{backend_slug}/theory", json={}).raise_for_status()
    baseline = client.get("/api/course").json()
    assert baseline["ai"]["summary"]["completed"] == 0
    assert baseline["ai"]["summary"]["total"] == sum(len(module["lessons"]) for module in baseline["ai"]["modules"])
    assert sum(stage["planned"] for stage in baseline["ai"]["roadmap"]) + baseline["ai"]["summary"]["total"] == 72
    assert slug not in {item["slug"] for module in baseline["modules"] for item in module["lessons"]}
    lesson = client.get(f"/api/lessons/{slug}").json()
    assert lesson["workspace_kind"] == "python"
    assert set(lesson["files"]) == {"main.py", "public_cases.py"}
    assert not lesson["has_task"] and lesson["has_solution"]
    assert "tests" not in lesson and "hidden_tests" not in lesson
    assert client.get("/api/lessons/ai01-ai-task-and-baseline").status_code == 404
    assert client.post(f"/api/check", json={"lesson_slug": slug, "files": lesson["files"]}).status_code == 409
    client.post(f"/api/lessons/{slug}/open").raise_for_status()
    assert client.post(f"/api/progress/{slug}/theory", json={}).json()["xp_awarded"] == 5
    assert client.post(f"/api/progress/{slug}/theory", json={}).json()["xp_awarded"] == 0
    after = client.get("/api/course").json()
    assert after["summary"] == {**baseline["summary"], "xp": baseline["summary"]["xp"] + 5}
    assert after["summary"]["last_opened_lesson"] == backend_slug
    assert after["modules"] == baseline["modules"]
    assert after["ai"]["summary"]["completed"] == 1
    assert after["ai"]["summary"]["percent"] == round(100 / after["ai"]["summary"]["total"])
    assert client.get(f"/api/lessons/{backend_slug}").json()["files"] == files


def test_ai_check_feedback_hides_cases_and_completes_only_requested_lesson(client, monkeypatch):
    slug = "ai03-direct-provider-adapter"
    private = "private test source and fixture values"
    skipped = True

    async def runner(payload):
        assert "--tb=no" in payload["command"] and "tests/test_main.py" in payload["tests"]
        return {
            "stdout": private, "stderr": private, "exit_code": 0, "duration_ms": 10, "timed_out": False,
            "tests_total": 2, "tests_passed": 1 if skipped else 2,
            "tests": [
                {"name": "case_a[private]", "status": "passed", "passed": True},
                {"name": "case_b[private]", "status": "skipped" if skipped else "passed", "passed": not skipped},
            ],
        }

    monkeypatch.setattr(main_module, "execute_in_runner", runner)
    payload = {"lesson_slug": slug, "files": {"main.py": "print('saved')"}}
    rejected = client.post("/api/check", json=payload).json()
    assert not rejected["passed"] and rejected["xp_awarded"] == 0
    assert "private" not in str(rejected)
    skipped = False
    accepted = client.post("/api/check", json=payload).json()
    assert accepted["passed"] and accepted["xp_awarded"] == 20
    assert client.post("/api/check", json=payload).json()["xp_awarded"] == 0
    assert client.get(f"/api/lessons/{slug}").json()["progress"]["task_completed"]
    assert not client.get("/api/lessons/ai03-messages-and-instructions").json()["progress"]["task_completed"]
    course = client.get("/api/course").json()
    assert course["ai"]["summary"]["completed"] == 1 and course["summary"]["completed"] == 0
