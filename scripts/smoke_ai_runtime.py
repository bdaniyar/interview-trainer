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


# Deliberate behavior changes with varied inputs. Each must fail the real grader.
NEGATIVE_CONTROLS = {
    "AI3.1": ('    try:\n        response =', '    return GenerationResult("completed", "fixed")\n    try:\n        response ='),
    "AI3.2": ('return Request(POLICY, items, ALLOWED_TOOLS)', 'return Request(external_note or POLICY, items, ALLOWED_TOOLS)'),
    "AI3.3": ('await client.aclose()', 'pass'),
    "AI3.4": ('{429, 503}', '{401, 429, 503}'),
    "AI3.5": ('await source.aclose()', 'pass'),
    "AI3.6": ('total <= budget', 'total < budget'),
    "AI3.7": ('status=answer.status, usage=answer.usage)', 'status=answer.status, text=answer.text, usage=answer.usage)'),
    "AI3.8": ('    assert offline.socket_calls == 0 and not offline.secret_seen\n', ''),
}


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
        if graded:
            original, flawed = NEGATIVE_CONTROLS[item["number"]]
            assert reference["main.py"].count(original) == 1
            mutant = reference["main.py"].replace(original, flawed)
            negative = call("/api/check", {**request, "files": {**reference, "main.py": mutant}})
            assert not negative["passed"] and not negative["timed_out"] and negative["xp_awarded"] == 0, negative
            assert negative["tests_total"] == failed["tests_total"] > 0
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
    guard = call("/api/run", {
        "lesson_slug": published[0][1]["slug"],
        "files": {"main.py": "from pathlib import Path\nassert {p.name for p in Path('/sys/class/net').iterdir()} == {'lo'}\nassert not Path('/var/run/docker.sock').exists()\nassert not Path('/data/pythoria.db').exists()\nprint('offline boundary confirmed')"},
    })
    assert guard["exit_code"] == 0 and "offline boundary confirmed" in guard["stdout"], guard
    # Restore the preview exercise program after the isolation probe.
    stage, first = published[0]
    call("/api/lessons/" + first["slug"] + "/files", {
        "files": {**files(ROOT / "content" / stage / first["slug"] / "solution"), "notes.py": "# Learner draft"},
    }, method="PUT")
    restored = call("/api/lessons/is-vs-eq")
    assert restored["files"] == backend["files"] and restored["progress"] == backend["progress"]
    assert call("/api/sql/lessons/s10-select-aliases-and-expressions")["completed"] == sql["completed"]
    assert call("/api/course")["summary"]["completed"] == catalog["summary"]["completed"]


if __name__ == "__main__":
    main()
