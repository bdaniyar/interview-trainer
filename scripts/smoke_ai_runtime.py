"""Exercise published AI workspaces through the disposable Docker API."""

import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("AI_TEST_API_ORIGIN", "http://127.0.0.1:18080")
origin = urlsplit(BASE)
if (
    origin.scheme != "http" or origin.hostname not in {"localhost", "127.0.0.1"}
    or not origin.port or origin.port < 10000 or origin.path or origin.query or origin.fragment
):
    raise SystemExit("Укажи адрес одноразового preview на loopback и тестовом порту")


def call(path, data=None, method=None, status=200):
    request = Request(
        BASE + path, data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"},
        method=method or ("POST" if data is not None else "GET"),
    )
    try:
        with urlopen(request, timeout=30) as response:
            assert response.status == status
            return json.load(response)
    except HTTPError as error:
        if error.code == status:
            return json.load(error)
        raise AssertionError((path, error.code, error.read())) from None


def files(directory):
    return {str(path.relative_to(directory)): path.read_text()
            for path in directory.rglob("*") if path.is_file() and path.suffix == ".py"}


def main():
    catalog = call("/api/course")
    backend = call("/api/lessons/is-vs-eq")
    sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    manifest = json.loads((ROOT / "content/ai_curriculum.json").read_text())
    published = [(stage["slug"], item) for stage in manifest["stages"]
                 for item in stage["lessons"] if item["status"] == "published"]
    assert catalog["ai"]["summary"]["total"] == len(published)
    for module, item in published:
        slug = item["slug"]
        path = "/api/lessons/" + slug
        lesson = call(path)
        directory = ROOT / "content" / module / slug
        starter = files(directory / "starter")
        reference = files(directory / "solution")
        assert "hidden_tests" not in lesson and "tests" not in lesson
        assert lesson["workspace_kind"] == "python"
        request = {"lesson_slug": slug, "files": starter}
        graded = item["practice"] == "graded"
        failed = call("/api/check", request, status=200 if graded else 409)
        if graded:
            assert not failed["passed"] and not failed["timed_out"], failed
            assert failed["xp_awarded"] == 0 and failed["tests_total"] > 0, failed
        payload = {**request, "files": {**reference, "notes.py": "# Learner draft"}}
        output = call("/api/run", payload)
        assert output["exit_code"] == 0 and not output["timed_out"], output
        if graded:
            complete = call("/api/check", payload)
            assert complete["passed"] and complete["tests_passed"] == complete["tests_total"] > 0, complete
            assert complete["xp_awarded"] == (0 if lesson["progress"]["task_completed"] else 20)
            assert call("/api/check", payload)["xp_awarded"] == 0
            progress = call(path)["progress"]
            assert progress["task_completed"] and progress["status"] == "completed"
        assert call(path)["files"] == payload["files"]
        print(json.dumps({"lesson": item["number"], "run": True, "saved": True,
                          "check_cases": complete["tests_total"] if graded else None}), flush=True)
    restored = call("/api/lessons/is-vs-eq")
    assert restored["files"] == backend["files"] and restored["progress"] == backend["progress"]
    assert call("/api/sql/lessons/s10-select-aliases-and-expressions")["completed"] == sql["completed"]
    assert call("/api/course")["summary"]["completed"] == catalog["summary"]["completed"]


if __name__ == "__main__":
    main()
