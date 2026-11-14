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
FILTER_TASKS = [
    ("s10-where-and-boolean-logic", "sql.basic.01", "SELECT id,email FROM users WHERE active = true",
     "SELECT id,email FROM users", "фильтрации", "(1,'a@example.com'),(2,'b@example.com'),(4,'d@example.com')"),
    ("s10-null-and-three-valued-logic", "sql.basic.03", "SELECT id,email FROM users WHERE country IS NULL",
     "SELECT id,email FROM users WHERE country = NULL", "NULL", "(3,'c@example.com')"),
]
ORDERED_TASKS = [
    ("s10-order-by-limit-and-offset", "sql.basic.04",
     "SELECT id,created_at FROM orders ORDER BY created_at DESC,id DESC LIMIT 2",
     "SELECT id,created_at FROM orders ORDER BY created_at DESC LIMIT 2",
     "SELECT * FROM (VALUES (14::bigint,TIMESTAMPTZ '2026-02-05'),(13::bigint,TIMESTAMPTZ '2026-02-04')) v(id,created_at) ORDER BY created_at DESC,id DESC",
     [["14", "2026-02-05T00:00:00Z"], ["13", "2026-02-04T00:00:00Z"]], "сортировки"),
    ("s10-distinct", "sql.basic.05",
     "SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country",
     "SELECT country FROM users WHERE country IS NOT NULL ORDER BY country",
     "SELECT country FROM (VALUES ('GE'),('KZ')) v(country) ORDER BY country",
     [["GE"], ["KZ"]], "повторы"),
]
PYTHON_FILES = {
    "main.py": "def compare_objects(a, b):\n    return {'same_identity': a is b, 'same_value': a == b}\n",
    "notes.py": "SAVED_FILE = 'preserve me'\nif __name__ == '__main__':\n    print('python stays available')\n",
}


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


def grade_task(slug, task_id, query, request_id=None, expected=200):
    answer = call(f"/api/sql/lessons/{slug}/tasks/{task_id}/check",
                  {"request_id": request_id or str(uuid4()), "sql": query}, expected=expected)
    assert not {"reference_sql", "seed", "rows", "columns", "container_id", "session_id"}.intersection(answer)
    for item in answer.get("feedback", []):
        assert set(item) == {"code", "message", "sqlstate"}
    wire = json.dumps(answer)
    assert "@example.com" not in wire and "@example.test" not in wire
    return answer


def solve_filtering_tasks():
    for index, (slug, task_id, correct, wrong, feedback, literals) in enumerate(FILTER_TASKS):
        assert call(f"/api/lessons/{slug}")["workspace_kind"] == "sql"
        assert not call(f"/api/sql/lessons/{slug}")["completed"]
        session = call("/api/sql/sessions", {"lesson_slug": slug}, expected=201)
        assert session["task_id"] == task_id and session["dataset_id"] == "shop-v1"
        path, generation = "/api/sql/sessions/" + session["session_id"], session["generation"]
        try:
            catalog = call(path + f"/catalog?generation={generation}")
            baseline = call(path + "/run", {"generation": generation, "sql": "SELECT * FROM users ORDER BY id"})
            assert len(baseline["rows"]) == 4
            failed = grade_task(slug, task_id, wrong)
            assert not failed["passed"] and not failed["completed"]
            assert feedback in failed["feedback"][0]["message"]
            token = str(uuid4())
            passed = grade_task(slug, task_id, correct + " ORDER BY id DESC", token)
            assert passed["passed"] and passed["completed"] and passed["tests_passed"] == passed["tests_total"] == 5
            assert grade_task(slug, task_id, correct + " ORDER BY id DESC", token) == passed
            hardcoded = grade_task(slug, task_id, f"SELECT * FROM (VALUES {literals}) v(id,email)")
            assert not hardcoded["passed"] and hardcoded["completed"] and hardcoded["tests_passed"] == 1
            columns = grade_task(slug, task_id, "SELECT id AS user_id,email FROM users")
            assert not columns["passed"] and "id, email" in columns["feedback"][0]["message"]
            assert "user_id" not in columns["feedback"][0]["message"]
            grade_task(slug, TASK_ID, correct, expected=404)
            assert call(path + f"/catalog?generation={generation}") == catalog
            assert call(path + "/run", {"generation": generation, "sql": "SELECT * FROM users ORDER BY id"})["rows"] == baseline["rows"]
            generation = call(path + "/reset", {"generation": generation})["generation"]
            assert call(f"/api/sql/lessons/{slug}")["completed"]
            if index == 0:
                assert not call(f"/api/sql/lessons/{FILTER_TASKS[1][0]}")["completed"]
        finally:
            call(path + f"?generation={generation}", method="DELETE", expected=204)
    assert call(f"/api/sql/lessons/{SLUG}")["completed"]
    print("WHERE/NULL HTTP smoke passed: independent 5/5 grades/progress, hardcoded 1/5, task-aware feedback, unchanged Explorer, Reset and cross-task rejection")


def solve_ordered_tasks():
    for index, (slug, task_id, correct, wrong, hardcoded_sql, rows, feedback) in enumerate(ORDERED_TASKS):
        lesson_before = call(f"/api/lessons/{slug}")
        assert lesson_before["workspace_kind"] == "sql"
        manifest = call(f"/api/sql/lessons/{slug}")
        assert manifest["task_id"] == task_id and not manifest["completed"]
        session = call("/api/sql/sessions", {"lesson_slug": slug}, expected=201)
        assert session["task_id"] == task_id
        path, generation = "/api/sql/sessions/" + session["session_id"], session["generation"]
        try:
            catalog = call(path + f"/catalog?generation={generation}")
            result = call(path + "/run", {"generation": generation, "sql": correct})
            assert result["error"] is None and result["rows"] == rows
            assert [c["name"] for c in result["columns"]] == manifest["expected_columns"]
            assert not call(f"/api/sql/lessons/{slug}")["completed"]  # Run is not Check.
            failed = grade_task(slug, task_id, wrong)
            assert not failed["passed"] and not failed["completed"] and failed["tests_passed"] < 6
            assert feedback in failed["feedback"][0]["message"]
            token = str(uuid4())
            passed = grade_task(slug, task_id, correct, token)
            assert passed["passed"] and passed["completed"] and passed["tests_passed"] == passed["tests_total"] == 6
            assert grade_task(slug, task_id, correct, token) == passed
            grade_task(slug, task_id, correct + " OFFSET 1", token, expected=409)
            hardcoded = grade_task(slug, task_id, hardcoded_sql)
            assert not hardcoded["passed"] and hardcoded["completed"] and hardcoded["tests_passed"] == 1
            assert call(path + f"/catalog?generation={generation}") == catalog
            assert call(path + "/run", {"generation": generation, "sql": correct})["rows"] == rows
            generation = call(path + "/reset", {"generation": generation})["generation"]
            assert call(f"/api/sql/lessons/{slug}")["completed"]
            if index == 0:
                assert not call(f"/api/sql/lessons/{ORDERED_TASKS[1][0]}")["completed"]
        finally:
            call(path + f"?generation={generation}", method="DELETE", expected=204)
        assert call(f"/api/lessons/{slug}")["files"] == lesson_before["files"]
    for slug in [SLUG] + [t[0] for t in FILTER_TASKS + ORDERED_TASKS]:
        assert call(f"/api/sql/lessons/{slug}")["completed"]
    print("ORDER/DISTINCT HTTP smoke passed: five lessons complete independently; correct 6/6, hardcoded 1/6, ordered Run, safe feedback, replay/conflict, Reset and Explorer isolation")


def main():
    if "--sql-offline" in sys.argv:
        assert call("/api/health")["status"] == "ok"
        response = call("/api/sql/sessions", {"lesson_slug": SLUG}, expected=503)
        assert response["error"]["code"] == "runner_unavailable"
        call(CHECK, {"request_id": str(uuid4()), "sql": SOLUTION}, expected=503)
        for slug, task_id, correct, *_ in FILTER_TASKS + ORDERED_TASKS:
            grade_task(slug, task_id, correct, expected=503)
        before = call("/api/course")["summary"]["xp"]
        result = call("/api/run", {"lesson_slug": "is-vs-eq", "files": PYTHON_FILES, "entrypoint": "notes.py"})
        assert result["exit_code"] == 0 and result["stdout"] == "python stays available\n"
        checked = call("/api/check", {"lesson_slug": "is-vs-eq", "files": PYTHON_FILES})
        assert checked["passed"] and checked["tests_total"] == 3 and checked["xp_awarded"] == 0
        assert call("/api/course")["summary"]["xp"] == before
        assert call("/api/lessons/is-vs-eq")["files"] == PYTHON_FILES
        print("SQL outage smoke passed: SQL Run/Check sanitized 503; real Python Docker Run AND Check remain available; files and XP preserved")
        return
    # Seed real Python progress/files in this stack's disposable SQLite only.
    python_files = PYTHON_FILES
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
            return grade_task(SLUG, TASK_ID, query, request_id, expected)

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
    solve_filtering_tasks()
    solve_ordered_tasks()
    assert call(f"/api/lessons/{SLUG}")["files"] == original["files"]
    assert call("/api/lessons/is-vs-eq")["files"] == python_before["files"] == python_files
    assert call("/api/lessons/is-vs-eq")["progress"] == python_before["progress"]
    assert call("/api/course")["summary"] == before
    assert check(SOLUTION)["passed"]  # No interactive session required.
    print("SQL Workspace/Check HTTP smoke passed: correct 4/4, hardcoded 1/4, failed/replay/sticky progress, unchanged Explorer; Run/Reset/Close and Python Check/files/progress/XP preserved")


if __name__ == "__main__":
    main()
