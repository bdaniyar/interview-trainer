"""HTTP assertions for docker-compose.sql-workspace-test.yml's disposable DB."""
import json
import sys
from uuid import uuid4
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = "http://localhost:18080"
SLUG = "s10-select-aliases-and-expressions"
TASK_ID = "sql.guided.10.2.projection.v1"
CHECK = f"/api/sql/lessons/{SLUG}/tasks/{TASK_ID}/check"
SOLUTION = "SELECT id AS user_id,email FROM users ORDER BY id DESC"


def call(path, data=None, method=None, expected=200):
    request = Request(BASE + path, data=json.dumps(data).encode() if data is not None else None,
                      method=method or ("POST" if data is not None else "GET"),
                      headers={"Content-Type": "application/json"})
    try:
        response = urlopen(request, timeout=120)
    except HTTPError as error:
        response = error
    with response:
        wire = response.read()
        assert response.status == expected, (path, response.status, wire)
        return json.loads(wire) if wire else None


def main():
    if "--sql-offline" in sys.argv:
        assert call("/api/health")["status"] == "ok"
        response = call("/api/sql/sessions", {"lesson_slug": SLUG}, expected=503)
        assert response["error"]["code"] == "runner_unavailable"
        call(CHECK, {"request_id": str(uuid4()), "sql": SOLUTION}, expected=503)
        result = call("/api/run", {"lesson_slug": "is-vs-eq", "files": {"main.py": "print('python stays available')\n"}, "entrypoint": "main.py"})
        assert result["exit_code"] == 0 and result["stdout"] == "python stays available\n"
        print("SQL outage smoke passed: Run/Check sanitized 503; backend and Python Docker Run remain available")
        return
    # Seed real Python progress/files in this stack's disposable SQLite only.
    python_files = {"main.py": "def compare_objects(a, b):\n    return {'same_identity': a is b, 'same_value': a == b}\n",
                    "notes.py": "SAVED_FILE = 'preserve me'\n"}
    python_check = call("/api/check", {"lesson_slug": "is-vs-eq", "files": python_files})
    assert python_check["passed"] and python_check["tests_total"] == 3
    call("/api/progress/generators/theory", {"completed": True})
    python_before = call("/api/lessons/is-vs-eq")
    original = call(f"/api/lessons/{SLUG}")
    before = call("/api/course")["summary"]
    lesson = call(f"/api/sql/lessons/{SLUG}")
    assert lesson["can_check"] is True and lesson["task_id"] == TASK_ID and not lesson["completed"]
    assert lesson["expected_columns"] == ["user_id", "email"]
    assert "solution_sql" not in lesson
    assert original["workspace_kind"] == "sql"
    session = call("/api/sql/sessions", {"lesson_slug": SLUG}, expected=201)
    path, generation = "/api/sql/sessions/" + session["session_id"], session["generation"]
    try:
        def run(query, expected=200, version=None):
            return call(path + "/run", {"generation": version or generation, "sql": query}, expected=expected)

        result = run("SELECT id,email FROM users ORDER BY id")
        assert result["error"] is None and result["rows"][0] == ["1", "a@example.com"] and len(result["rows"]) == 4
        joined = run("SELECT u.email,o.total FROM users u JOIN orders o ON u.id=o.user_id WHERE o.status='paid' ORDER BY o.total DESC LIMIT 1")
        assert joined["rows"] == [["b@example.com", "200.00"]]
        catalog = call(path + f"/catalog?generation={generation}")
        tables = {table["name"]: table for table in catalog["tables"]}
        assert len(tables) == 4 and tables["order_items"]["primary_key"] == ["order_id", "product_id"]
        assert tables["users"]["foreign_keys"][0]["referenced_table"] == "users"
        handle = tables["users"]["handle"]
        assert len(call(path + f"/tables/{handle}/rows?generation={generation}")["rows"]) == 4

        def check(query, request_id=None, expected=200):
            answer = call(CHECK, {"request_id": request_id or str(uuid4()), "sql": query}, expected=expected)
            wire = json.dumps(answer)
            assert not {"reference_sql", "seed", "rows", "columns", "container_id", "session_id"}.intersection(answer)
            for item in answer.get("feedback", []):
                assert set(item) == {"code", "message", "sqlstate"}
            assert "@example.com" not in wire and "@example.test" not in wire
            return answer

        token = str(uuid4())
        passed = check(SOLUTION, token)
        assert passed["passed"] and passed["completed"] and passed["tests_passed"] == passed["tests_total"] == 4
        assert check(SOLUTION, token) == passed
        check("SELECT 1", token, expected=409)
        for wrong in ["SELECT id,email FROM users", "SELECT email,id AS user_id FROM users",
                      "SELECT id AS user_id,email FROM users LIMIT 1",
                      "SELECT id AS user_id,email FROM users UNION ALL SELECT id AS user_id,email FROM users",
                      "SELECT 1 AS user_id,'a@example.com' AS email"]:
            failed = check(wrong)
            assert not failed["passed"] and failed["completed"] and failed["tests_passed"] < 4
        # Exact public rows still fail the other three fixture revisions.
        literals = ",".join(f"({row[0]},'{row[1]}')" for row in result["rows"])
        hardcoded = check(f"SELECT user_id,email FROM (VALUES {literals}) AS v(user_id,email)")
        assert not hardcoded["passed"] and hardcoded["tests_passed"] == 1
        cast_error = check("SELECT id AS user_id,email::bigint AS email FROM users")
        assert not cast_error["passed"] and cast_error["feedback"][0]["sqlstate"] == "22P02"
        assert call(f"/api/sql/lessons/{SLUG}")["completed"]
        assert call(path + f"/catalog?generation={generation}") == catalog
        assert run("SELECT id,email FROM users ORDER BY id")["rows"] == result["rows"]
        assert len(call(path + f"/tables/{handle}/rows?generation={generation}")["rows"]) == 4
        call(path + f"/tables/forged/rows?generation={generation}", expected=404)
        assert run("SELECT count(*) FROM users")["rows"] == [["4"]]
        assert run("DELETE FROM users")["error"]["kind"] == "policy"
        assert run("SELECT missing FROM users")["error"]["sqlstate"] == "42703"
        assert run("SELECT g FROM generate_series(1,10000) g")["rows_returned"] == 500
        reset = call(path + "/reset", {"generation": generation})
        generation = reset["generation"]
        run("SELECT 1", expected=409, version=generation - 1)
        call(path + f"/tables/{handle}/rows?generation={generation}", expected=404)
        assert run("SELECT count(*) FROM users")["rows"] == [["4"]]
    finally:
        call(path + f"?generation={generation}", method="DELETE", expected=204)
    assert call(f"/api/lessons/{SLUG}")["files"] == original["files"]
    assert call("/api/lessons/is-vs-eq")["files"] == python_before["files"] == python_files
    assert call("/api/lessons/is-vs-eq")["progress"] == python_before["progress"]
    assert call("/api/course")["summary"] == before
    assert check(SOLUTION)["passed"]  # No interactive session required.
    print("SQL Workspace/Check HTTP smoke passed: correct 4/4, hardcoded 1/4, failed/replay/sticky progress, unchanged Explorer; Run/Reset/Close and Python Check/files/progress/XP preserved")


if __name__ == "__main__":
    main()
