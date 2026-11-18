"""HTTP integration against the disposable Compose workspace on port 18080."""
import argparse
from http.client import HTTPConnection
import json
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

from smoke_sql_workspace import BASE

DML = "s10-data-modification"
BOOKING = "s11-booking-concurrency"
TASKS = {
    DML: "pg.write.10.25.status-v1",
    BOOKING: "pg.tx.11.17.booking-v1",
}
REFERENCES = {
    DML: "UPDATE orders SET status='paid' WHERE id=10 RETURNING id,status",
    BOOKING: """BEGIN;
WITH claimed AS (
 UPDATE inventory SET available=available-1 WHERE id=1 AND available>0 RETURNING id
)
INSERT INTO reservations(request_key,room_id)
SELECT 'REQUEST_KEY',id FROM claimed RETURNING request_key,room_id;
COMMIT;""",
}


def call(path, payload=None, *, method=None, status=200):
    request = Request(BASE + path, data=json.dumps(payload).encode() if payload is not None else None,
                      headers={"Content-Type": "application/json"}, method=method)
    try:
        with urlopen(request, timeout=135) as response:
            code, body = response.status, response.read()
    except HTTPError as error:
        code, body = error.code, error.read()
    assert code == status, (path, code, body[:800])
    return json.loads(body)


def lesson(slug):
    return "/api/transactions/lessons/" + slug


def check(slug, sql, request_id, status=200):
    return call(lesson(slug) + "/tasks/" + TASKS[slug] + "/check",
                {"request_id": request_id, "sql": sql}, status=status)


def observe(path, generation, test):
    deadline = monotonic() + 4
    while monotonic() < deadline:
        result = call(path + f"?generation={generation}")
        if test(result):
            return result
        sleep(.03)
    raise AssertionError(result)


def live():
    assert call("/api/lessons/" + DML)["workspace_kind"] == "transaction"
    xp = call("/api/course")["summary"]["xp"]
    python = call("/api/lessons/is-vs-eq")
    old_sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    session = call(lesson(BOOKING) + "/sessions", {}, status=201)
    sid = session["session_id"]
    path = lesson(BOOKING) + "/sessions/" + sid
    generation = session["generation"]

    def run(side, source, expected=202):
        return call(path + "/run", dict(generation=generation, side=side, sql=source), status=expected)

    try:
        assert set(session) == {"session_id", "generation", "remaining_ms"}
        assert call(lesson(DML) + "/sessions/" + sid + "?generation=1",
                    status=409)["error"]["code"] == "stale_session"
        assert run("A", "CREATE TABLE example(a int)", 422)["error"]["code"] == "policy"
        run("A", "BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE")
        observe(path, generation, lambda value: value["states"]["A"] == "transaction")
        client = HTTPConnection("localhost", 18080, timeout=3)
        try:
            client.request("POST", path + "/run", body=json.dumps(dict(
                generation=generation, side="B", sql="SELECT id FROM inventory WHERE id=1 FOR UPDATE")),
                headers={"Content-Type": "application/json"})
        finally:
            client.close()
        blocked = observe(path, generation, lambda value: value["pending"].get("B", {}).get("blockers") == ["A"])
        op = blocked["pending"]["B"]["operation"]
        run("A", "COMMIT")
        final = observe(path, generation, lambda value: not value["pending"])
        assert any(event["phase"] == "result" and event.get("operation") == op for event in final["timeline"])
        reset = call(path + "/reset", {"generation": generation})
        assert reset["session_id"] == sid and reset["generation"] == generation + 1
        generation = reset["generation"]
        assert call(path + "?generation=1", status=409)["error"]["code"] == "stale_session"
    finally:
        call(path + f"?generation={generation}", method="DELETE")

    ids = {}
    for slug in TASKS:
        last = str(uuid4())
        result = check(slug, REFERENCES[slug], last)
        assert result["passed"] and result["tests_passed"] == 6 and result["completed"]
        assert check(slug, REFERENCES[slug], last) == result
        assert check(slug, "SELECT 1", last, 409)["error"]["code"] == "request_conflict"
        wrong = "UPDATE orders SET status='paid' RETURNING id,status" if slug == DML else "SELECT 'request-A'::text AS request_key, 1::bigint AS room_id"
        failed = check(slug, wrong, str(uuid4()))
        assert not failed["passed"] and failed["completed"]
        assert call(lesson(slug))["completed"]
        ids[slug] = last
    completed_session = call(lesson(DML) + "/sessions", {}, status=201)
    completed_path = lesson(DML) + "/sessions/" + completed_session["session_id"]
    generation = completed_session["generation"]
    try:
        generation = call(completed_path + "/reset", {"generation": generation})["generation"]
        assert call(lesson(DML))["completed"]
    finally:
        call(completed_path + f"?generation={generation}", method="DELETE")
    demo = call(lesson("s11-deadlocks") + "/scenario", {"name": "deadlock"})
    assert "40P01" in demo["states"] and demo["connections"] == 2
    demo = call(lesson("s11-isolation-levels") + "/scenario", {"name": "serializable"})
    assert "40001" in demo["states"] and demo["connections"] == 2
    assert call("/api/course")["summary"]["xp"] == xp
    assert call("/api/lessons/is-vs-eq") == python
    assert call("/api/sql/lessons/s10-select-aliases-and-expressions") == old_sql
    print(json.dumps(dict(observedBlocking=True, disconnectedClient=True, resetGeneration=True, checks=2,
                          sixCasesEach=True, replay=True, completionSticky=True,
                          oldProgressPreserved=True, xpPreserved=True)))
    return ids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save-replays")
    parser.add_argument("--verify-replays")
    args = parser.parse_args()
    if args.verify_replays:
        with open(args.verify_replays) as file:
            replay_ids = json.load(file)
        for slug, saved in replay_ids.items():
            assert call(lesson(slug))["completed"]
            assert check(slug, REFERENCES[slug], saved)["passed"]
        print("Transaction progress and request replay survived backend restart.")
    else:
        ids = live()
        if args.save_replays:
            with open(args.save_replays, "w") as file:
                json.dump(ids, file)


if __name__ == "__main__":
    main()
