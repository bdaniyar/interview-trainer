"""Real HTTP/Python Docker smoke on the disposable workspace stack only."""

import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:18080"
ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    "s20-fastapi-backgroundtasks": 7,
    "s20-retry-and-backoff": 17,
    "s20-idempotency": 10,
    "s20-periodic-tasks": 14,
    "s20-delivery-semantics": 14,
}


def call(path, data=None, method=None):
    request = Request(
        BASE + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"},
        method=method or ("POST" if data is not None else "GET"),
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        raise AssertionError((path, error.code, error.read())) from None


def main():
    baseline = call("/api/course")["summary"]["xp"]
    old = call("/api/lessons/is-vs-eq")
    old_sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    for i, (slug, count) in enumerate(TASKS.items(), 1):
        lesson = call("/api/lessons/" + slug)
        assert (
            lesson["has_task"]
            and lesson["has_solution"]
            and lesson["workspace_kind"] == "python"
        ), lesson
        assert "tests" not in lesson and "hidden_tests" not in lesson
        root = ROOT / "content/stage-20" / slug
        starter = {
            "lesson_slug": slug,
            "files": {"main.py": (root / "starter/main.py").read_text()},
            "entrypoint": "main.py",
        }
        wrong = call("/api/check", starter)
        assert (
            not wrong["passed"]
            and not wrong["timed_out"]
            and wrong["tests_total"] == count
            and wrong["tests_passed"] == 0
            and wrong["xp_awarded"] == 0
        ), wrong
        assert "Контракт проверки не выполнен" in wrong["stdout"], wrong
        assert "@pytest.mark.parametrize" not in wrong["stdout"]
        assert "assert backoff(" not in wrong["stdout"]
        assert "NotImplementedError:" not in wrong["stdout"]
        files = {
            "main.py": (root / "solution/main.py").read_text()
            + "\nif __name__ == '__main__':\n    print('worker-main-loaded')\n",
            "notes.py": "# keep this independent learner file\n",
        }
        payload = {"lesson_slug": slug, "files": files, "entrypoint": "main.py"}
        run = call("/api/run", payload)
        assert (
            run["exit_code"] == 0
            and not run["timed_out"]
            and "worker-main-loaded" in run["stdout"]
        ), run
        correct = call("/api/check", payload)
        assert (
            correct["passed"]
            and correct["tests_passed"] == correct["tests_total"] == count
            and correct["xp_awarded"] == 20
        ), correct
        replay = call("/api/check", payload)
        assert replay["passed"] and replay["xp_awarded"] == 0, replay
        retry = call("/api/check", starter)
        assert not retry["passed"] and retry["xp_awarded"] == 0, retry
        assert call("/api/lessons/" + slug)["progress"]["task_completed"]
        call("/api/lessons/" + slug + "/files", {"files": files}, "PUT")
        assert call("/api/lessons/" + slug)["files"] == files
        assert call("/api/course")["summary"]["xp"] == baseline + 20 * i
        print(
            json.dumps(
                dict(
                    slug=slug,
                    run=True,
                    correct=count,
                    starter=0,
                    replayXp=0,
                    failedRetrySticky=True,
                    twoFilesPreserved=True,
                )
            ),
            flush=True,
        )
    current = call("/api/lessons/is-vs-eq")
    assert current["files"] == old["files"] and current["progress"] == old["progress"]
    current_sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    assert current_sql["completed"] == old_sql["completed"]
    print(
        json.dumps(
            dict(
                workerExercises=5,
                referenceTests=62,
                existingPythonAndSqlPreserved=True,
                pythonXpDelta=100,
            )
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
