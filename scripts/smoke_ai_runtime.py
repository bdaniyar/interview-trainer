"""Exercise published AI workspaces through the disposable Docker API."""

import argparse
import json
import os
import time
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


def execute(path, payload):
    result = call(path, payload)
    if result["timed_out"]:
        print(f"Preview sandbox timed out for {payload['lesson_slug']} {path}; retrying once", flush=True)
        time.sleep(1)
        result = call(path, payload)
    return result


def files(directory):
    return {str(path.relative_to(directory)): path.read_text()
            for path in directory.rglob("*") if path.is_file() and path.suffix == ".py"}


# Deliberate behavior changes with varied inputs. Each must fail the real grader.
NEGATIVE_CONTROLS = {
    "AI6.10": ('if any(resolve(state, actor, ref) != text for ref, text in supplied.items()):', 'if False:'),
    "AI6.8": ('if claim.text not in support.get(ref, ()):', 'if False:'),
    "AI6.9": ('hits / len(relevant) if relevant else None', 'hits / k if relevant else None'),
    "AI6.6": ('enumerate(dict.fromkeys(ordered), 1)', 'enumerate(ordered, 1)'),
    "AI6.7": ('rows = retrieve(principal, question)', 'rows = ()'),
    "AI6.4": ('scope.subject == row.owner or scope.subject in row.readers', 'True'),
    "AI6.5": ('/ len(reference) if reference else None', '/ k if reference else None'),
    "AI6.1": ('return min(1.0, max(-1.0, similarity))', 'return abs(similarity)'),
    "AI6.2": ('row.space != space or not valid(space, row.vector)', 'not valid(space, row.vector)'),
    "AI6.3": ('start = stop - overlap', 'start = stop'),
    "AI5.7": ('rows = [await repository.read(number) for number in ids]',
              'return Observation(call.id, "ok", ((42, "confirmed"),))'),
    "AI5.5": ('if total + size + reserve > capacity:', 'if total + size > capacity:'),
    "AI5.6": ('    scope = SCOPES.get(name)', '    if name == "cancel_booking":\n        await store.cancel(44)\n    scope = SCOPES.get(name)'),
    "AI5.3": ('or policy.owner != principal.subject', 'or False'),
    "AI5.4": ('while steps < budget.steps:', 'while True:'),
    "AI5.1": ('by_id[call.call_id]', 'by_id[call.item_id]'),
    "AI5.2": ('await tool.read(principal, args)', '{"city": "Астана"}'),
    "AI4.5": ('and type(observed[field]) is type(expected[field])', 'and True'),
    "AI4.6": ('self.check_in>=self.check_out', 'self.check_in==self.check_out'),
    "AI4.3": ('getattr(response,"schema_version",None)!=expected_revision', 'getattr(response,"schema_version",None)=="blocked"'),
    "AI4.4": ('{"incomplete","malformed","retryable"}', '{"incomplete","malformed","retryable","refusal"}'),
    "AI4.1": ('Prompt(VERSION,POLICY,EXAMPLES,text,', 'Prompt(VERSION,note or POLICY,EXAMPLES,text,'),
    "AI4.2": ('self.check_out<=self.check_in', 'self.check_out==self.check_in'),
    "AI2.7": ('zip(tokens[1:],distributions', 'zip(tokens[:-1],distributions'),
    "AI2.9": ('left.model!=right.model or ', ''),
    "AI2.4": ('[max(0,z) for z in hidden]', 'hidden'),
    "AI2.6": ('available=k[:i+1] if causal else k', 'available=k'),
    "AI2.2": ('checked(right), strict=True', 'checked(right)'),
    "AI2.3": ('db=2*fsum(errors)/n', 'db=2*fsum(errors)'),
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson", action="append", default=[], help="Published lesson number, for example AI2.2")
    args = parser.parse_args()
    catalog = call("/api/course")
    backend = call("/api/lessons/is-vs-eq")
    sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    manifest = json.loads((ROOT / "content/ai_curriculum.json").read_text())
    published = [(stage["slug"], item) for stage in manifest["stages"]
                 for item in stage["lessons"] if item["status"] == "published"]
    assert catalog["ai"]["summary"]["total"] == len(published)
    selected = [(stage, item) for stage, item in published
                if not args.lesson or item["number"] in args.lesson]
    if not selected or set(args.lesson) - {item["number"] for _, item in selected}:
        parser.error("All selected lessons must be published")
    for module, item in selected:
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
        failed = execute("/api/check", request) if graded else call("/api/check", request, status=409)
        if graded:
            assert not failed["passed"] and not failed["timed_out"], failed
            assert failed["xp_awarded"] == 0 and failed["tests_total"] > 0, failed
        if graded:
            original, flawed = NEGATIVE_CONTROLS[item["number"]]
            assert reference["main.py"].count(original) == 1
            mutant = reference["main.py"].replace(original, flawed)
            negative = execute("/api/check", {**request, "files": {**reference, "main.py": mutant}})
            assert not negative["passed"] and not negative["timed_out"] and negative["xp_awarded"] == 0, negative
            assert negative["tests_total"] == failed["tests_total"] > 0
        payload = {**request, "files": {**reference, "notes.py": "# Learner draft"}}
        output = execute("/api/run", payload)
        assert output["exit_code"] == 0 and not output["timed_out"], output
        if graded:
            complete = execute("/api/check", payload)
            assert complete["passed"] and complete["tests_passed"] == complete["tests_total"] > 0, complete
            assert complete["xp_awarded"] == (0 if lesson["progress"]["task_completed"] else 20)
            repeat = execute("/api/check", payload)
            assert repeat["passed"] and repeat["xp_awarded"] == 0, repeat
            progress = call(path)["progress"]
            assert progress["task_completed"] and progress["status"] == "completed"
        assert call(path)["files"] == payload["files"]
        print(json.dumps({"lesson": item["number"], "run": True, "saved": True,
                          "check_cases": complete["tests_total"] if graded else None}), flush=True)
    # Some Linux kernels expose inert tunnel devices in an isolated namespace.
    # Ask for a route to documentation-only addresses without sending any data.
    probe = """
import errno
from pathlib import Path
import socket

for family, destination in (
    (socket.AF_INET, ("192.0.2.1", 9)),
    (socket.AF_INET6, ("2001:db8::1", 9)),
):
    try:
        with socket.socket(family, socket.SOCK_DGRAM) as sock:
            sock.connect(destination)
    except OSError as error:
        assert error.errno in {errno.ENETUNREACH, errno.EAFNOSUPPORT}, error
    else:
        raise AssertionError("Sandbox has an external route")

assert not Path("/var/run/docker.sock").exists()
assert not Path("/data/pythoria.db").exists()
print("offline boundary confirmed")
"""
    guard = execute("/api/run", {
        "lesson_slug": selected[0][1]["slug"],
        "files": {"main.py": probe},
    })
    assert guard["exit_code"] == 0 and "offline boundary confirmed" in guard["stdout"], guard
    # Restore the preview exercise program after the isolation probe.
    stage, first = selected[0]
    call("/api/lessons/" + first["slug"] + "/files", {
        "files": {**files(ROOT / "content" / stage / first["slug"] / "solution"), "notes.py": "# Learner draft"},
    }, method="PUT")
    restored = call("/api/lessons/is-vs-eq")
    assert restored["files"] == backend["files"] and restored["progress"] == backend["progress"]
    assert call("/api/sql/lessons/s10-select-aliases-and-expressions")["completed"] == sql["completed"]
    assert call("/api/course")["summary"]["completed"] == catalog["summary"]["completed"]


if __name__ == "__main__":
    main()
