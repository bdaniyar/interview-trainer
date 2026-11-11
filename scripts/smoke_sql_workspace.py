"""HTTP assertions for docker-compose.sql-workspace-test.yml's disposable DB."""
import json
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = "http://localhost:18080"
SLUG = "s10-select-aliases-and-expressions"


def call(path, data=None, method=None, expected=200):
    request = Request(BASE + path, data=json.dumps(data).encode() if data is not None else None,
                      method=method or ("POST" if data is not None else "GET"),
                      headers={"Content-Type": "application/json"})
    try:
        response = urlopen(request, timeout=40)
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
        result = call("/api/run", {"lesson_slug": "is-vs-eq", "files": {"main.py": "print('python stays available')\n"}, "entrypoint": "main.py"})
        assert result["exit_code"] == 0 and result["stdout"] == "python stays available\n"
        print("SQL outage smoke passed: sanitized 503; backend and Python Docker Run remain available")
        return
    original = call(f"/api/lessons/{SLUG}")
    before = call("/api/course")["summary"]
    lesson = call(f"/api/sql/lessons/{SLUG}")
    assert lesson["can_check"] is False and "solution_sql" not in lesson
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
    assert call("/api/course")["summary"] == before
    print("SQL Workspace HTTP smoke passed: Run/JOIN/catalog/browse/errors/limits/Reset/Close; Python files and progress unchanged")


if __name__ == "__main__":
    main()
