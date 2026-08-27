"""End-to-end smoke test for already running local services."""

from __future__ import annotations

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


API = "http://localhost:8000"


def request(path: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(f"{API}{path}", data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=15) as response:
            return response.status, json.loads(response.read())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read())


def main() -> None:
    assert request("/api/health")[1]["status"] == "ok"
    with urlopen("http://localhost:8001/health", timeout=5) as response:
        assert json.loads(response.read())["status"] == "ok"
    with urlopen("http://localhost:3000/", timeout=10) as response:
        assert response.status == 200

    course = request("/api/course")[1]
    assert course["summary"]["total"] == 359
    assert len(course["modules"]) >= 30
    interview = request("/api/interview")[1]
    assert len(interview["questions"]) == 25 and len(interview["sets"]) == 20
    lesson = request("/api/lessons/is-vs-eq")[1]
    assert lesson["has_task"] is True and "main.py" in lesson["files"]

    files = {"main.py": "print('Hello from runner')\n"}
    assert request("/api/lessons/is-vs-eq/files", "PUT", {"files": files})[0] == 200
    assert request("/api/lessons/is-vs-eq")[1]["files"] == files

    run = request("/api/run", "POST", {"lesson_slug": "is-vs-eq", "files": files, "entrypoint": "main.py"})[1]
    assert run["exit_code"] == 0 and run["stdout"] == "Hello from runner\n"

    syntax_files = {"main.py": "if True print('broken')\n"}
    syntax = request("/api/run", "POST", {"lesson_slug": "is-vs-eq", "files": syntax_files, "entrypoint": "main.py"})[1]
    assert syntax["exit_code"] != 0 and "SyntaxError" in syntax["stderr"]

    wrong_files = {"main.py": "def compare_objects(left, right):\n    return {}\n"}
    wrong = request("/api/check", "POST", {"lesson_slug": "is-vs-eq", "files": wrong_files, "entrypoint": "main.py"})[1]
    assert wrong["passed"] is False and wrong["tests_total"] == 3

    correct_files = {"main.py": "def compare_objects(left, right):\n    return {'same_identity': left is right, 'same_value': left == right}\n"}
    correct = request("/api/check", "POST", {"lesson_slug": "is-vs-eq", "files": correct_files, "entrypoint": "main.py"})[1]
    assert correct["passed"] is True and correct["tests_passed"] == correct["tests_total"] == 3

    terminal = request("/api/terminal", "POST", {"lesson_slug": "is-vs-eq", "files": correct_files, "command": "pwd"})[1]
    assert terminal["stdout"] == "/workspace\n"
    assert request("/api/course")[1]["summary"]["completed"] >= 1
    print("Smoke test passed: frontend, backend, runner, Run, Check, SQLite persistence, terminal")


if __name__ == "__main__":
    main()
