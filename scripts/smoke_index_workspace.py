"""Advanced lab API checks against the disposable Compose project only."""
from pathlib import Path
import json
import sys
from uuid import uuid4

from smoke_transaction_workspace import call

TASKS = {
    "s11-index-mental-model": "pg.index.11.4.expression-v1",
    "s11-postgresql-b-tree": "pg.index.11.5.workload-v1",
    "s11-composite-indexes-and-column-order": "pg.index.11.6.composite-v1",
    "s11-selectivity": "pg.index.11.7.partial-v1",
    "s11-explain-and-explain-analyze": "pg.plan.11.8.analysis-v1",
    "s11-pagination": "pg.plan.11.15.range-v1",
}
PATH = "/api/index-lab/lessons/s11-pagination"
REFERENCE = (
    "SELECT id, created_at FROM orders WHERE created_at >= TIMESTAMP '2026-11-08' "
    "AND created_at < TIMESTAMP '2026-11-09' ORDER BY created_at,id LIMIT 30"
)
INCREMENT = "/api/transactions/lessons/s11-mvcc-basics"


def main():
    mode, replay_file = sys.argv[1:]
    replay_file = Path(replay_file)
    if mode == "--verify-replays":
        payload = json.loads(replay_file.read_text())
        assert call(PATH + "/check", payload)["completed"] and call(PATH)["completed"]
        print("Advanced Check replay and completion survived backend restart.")
        return

    assert mode == "--save-replays"
    initial_xp = call("/api/course")["summary"]["xp"]
    python_lesson = call("/api/lessons/is-vs-eq")
    old_sql = call("/api/sql/lessons/s10-select-aliases-and-expressions")
    assert call("/api/lessons/s11-connection-pooling")["workspace_kind"] == "project"
    for slug, task_id in TASKS.items():
        assert call("/api/lessons/" + slug)["workspace_kind"] == "index"
        assert call("/api/index-lab/lessons/" + slug)["task_id"] == task_id
    assert call("/api/index-lab/lessons/s11-jsonb", status=404)["error"]["code"] == "unknown_task"
    assert call(PATH + "/run", {"sql": "CREATE TABLE x(i int)"}, status=422)["error"]["code"] == "policy"
    assert call(PATH + "/run", {"sql": REFERENCE, "case": "hidden"}, status=422)["error"]["code"] == "invalid_request"
    preview = call(PATH + "/run", {"sql": REFERENCE})
    assert preview["valid"]
    evidence, = preview["runs"]
    assert len(evidence["samples"]) == len(evidence["baseline_samples"]) == 3
    assert evidence["result"]["rows_returned"] == evidence["plan"]["Actual Rows"] == 30
    assert evidence["result"]["columns"][0]["pg_type"] == "int8"
    assert evidence["baseline_plan"] and evidence["controlled"]
    assert not call(PATH)["completed"]
    payload = {"sql": REFERENCE, "request_id": str(uuid4())}
    passed = call(PATH + "/check", payload)
    assert passed["passed"] and passed["completed"] and passed["tests_passed"] == 6
    assert call(PATH + "/check", payload) == passed
    edge = REFERENCE.replace("created_at < TIMESTAMP", "created_at <= TIMESTAMP")
    assert call(PATH + "/check", payload | {"sql": edge}, status=409)["error"]["code"] == "request_conflict"
    rejected = call(PATH + "/check", {"sql": edge, "request_id": str(uuid4())})
    assert rejected["completed"] and not rejected["passed"] and 1 <= rejected["tests_passed"] < 6
    increment = call(INCREMENT)
    task = increment["task_id"]
    assert task == "pg.tx.11.11.stock-increment-v1"
    report = call(INCREMENT + "/tasks/" + task + "/check", {
        "sql": "UPDATE inventory SET available=available+1 WHERE id=1 RETURNING id,available",
        "request_id": str(uuid4()),
    })
    assert report["passed"] and report["completed"] and report["tests_passed"] == 6
    assert call("/api/course")["summary"]["xp"] == initial_xp
    assert call("/api/lessons/is-vs-eq") == python_lesson
    assert call("/api/sql/lessons/s10-select-aliases-and-expressions") == old_sql
    replay_file.write_text(json.dumps(payload))
    print(json.dumps(dict(manifests=6, repeatPlans=True, dateBoundaryCheck=True,
                          idempotency=True, concurrentCheck=True, xpAndFilesPreserved=True)))


if __name__ == "__main__":
    main()
