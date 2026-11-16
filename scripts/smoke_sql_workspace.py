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
AGGREGATE_TASKS = [
    ("s10-aggregates", "sql.aggregation.09",
     "SELECT COUNT(*) AS orders_count FROM orders",
     "SELECT COUNT(*) AS orders_count FROM users",
     "SELECT 5::bigint AS orders_count", [["5"]], "источник"),
    ("s10-group-by", "sql.aggregation.10",
     "SELECT status,COUNT(*) AS count FROM orders GROUP BY status ORDER BY status",
     "SELECT status,COUNT(*) AS count FROM orders GROUP BY status ORDER BY status DESC",
     "SELECT * FROM (VALUES ('cancelled',1::bigint),('new',1::bigint),('paid',3::bigint)) v(status,count) ORDER BY status",
     [["cancelled", "1"], ["new", "1"], ["paid", "3"]], "групп"),
    ("s10-having", "sql.aggregation.13",
     "SELECT user_id,COUNT(*) AS count FROM orders GROUP BY user_id HAVING COUNT(*) >= 2 ORDER BY user_id",
     "SELECT user_id,COUNT(*) AS count FROM orders GROUP BY user_id HAVING COUNT(*) > 2 ORDER BY user_id",
     "SELECT * FROM (VALUES (1::bigint,2::bigint),(2::bigint,2::bigint)) v(user_id,count) ORDER BY user_id",
     [["1", "2"], ["2", "2"]], "минимум два"),
]
JOIN_TASKS = [
    ("s10-inner-join", "sql.join.17",
     "SELECT o.id AS order_id,u.email FROM orders o JOIN users u ON u.id=o.user_id ORDER BY o.id",
     "SELECT o.id AS order_id,u.email FROM orders o CROSS JOIN users u",
     "SELECT * FROM (VALUES (10::bigint,'a@example.com'),(11::bigint,'a@example.com'),(12::bigint,'b@example.com'),(13::bigint,'b@example.com'),(14::bigint,'d@example.com')) v(order_id,email)",
     [["10", "a@example.com"], ["11", "a@example.com"], ["12", "b@example.com"], ["13", "b@example.com"], ["14", "d@example.com"]], "ключ связи"),
    ("s10-left-join", "sql.join.18",
     "SELECT u.id,u.email FROM users u LEFT JOIN orders o ON o.user_id=u.id WHERE o.id IS NULL ORDER BY u.id",
     "SELECT u.id,u.email FROM users u LEFT JOIN orders o ON o.user_id=u.id WHERE o.id IS NOT NULL",
     "SELECT 3::bigint AS id,'c@example.com' AS email", [["3", "c@example.com"]], "отсутствие"),
    ("s10-right-and-full-outer-join", "sql.join.25",
     "SELECT p.id AS product_id,oi.order_id FROM order_items oi RIGHT JOIN products p ON p.id=oi.product_id ORDER BY p.id,oi.order_id",
     "SELECT p.id AS product_id,oi.order_id FROM order_items oi JOIN products p ON p.id=oi.product_id ORDER BY p.id,oi.order_id",
     "SELECT * FROM (VALUES (100::bigint,10::bigint),(100::bigint,14::bigint),(101::bigint,10::bigint),(101::bigint,12::bigint),(102::bigint,13::bigint)) v(product_id,order_id) ORDER BY product_id,order_id",
     [["100", "10"], ["100", "14"], ["101", "10"], ["101", "12"], ["102", "13"]], "товаров"),
    ("s10-self-join", "sql.join.20",
     "SELECT u.email,m.email AS manager_email FROM users u LEFT JOIN users m ON m.id=u.manager_id ORDER BY u.id",
     "SELECT u.email,m.email AS manager_email FROM users u JOIN users m ON m.id=u.manager_id ORDER BY u.id",
     "SELECT email,manager_email FROM (VALUES (1,'a@example.com',NULL::text),(2,'b@example.com','a@example.com'),(3,'c@example.com','a@example.com'),(4,'d@example.com','b@example.com')) v(id,email,manager_email) ORDER BY id",
     [["a@example.com", None], ["b@example.com", "a@example.com"], ["c@example.com", "a@example.com"], ["d@example.com", "b@example.com"]], "руководителем"),
]
ADVANCED_TASKS = [('s10-subqueries',
  'sql.subquery.27',
  'SELECT id,total FROM orders WHERE total > (SELECT AVG(total) FROM orders)',
  'SELECT id,total FROM orders WHERE total >= (SELECT AVG(total) FROM orders)',
  "SELECT * FROM (VALUES ('10'::int8,'100.00'::numeric),('12'::int8,'200.00'::numeric)) v(id,total)",
  [['10', '100.00'], ['12', '200.00']],
  'Учитывайте все заказы при расчёте среднего, строгую границу и пустой набор.'),
 ('s10-correlated-subquery',
  'sql.subquery.31',
  'SELECT o.id,o.user_id FROM orders o WHERE o.created_at=(SELECT MAX(i.created_at) FROM orders i WHERE '
  'i.user_id=o.user_id) ORDER BY o.user_id',
  'SELECT id,user_id FROM orders WHERE created_at=(SELECT MAX(created_at) FROM orders) ORDER BY user_id',
  "SELECT * FROM (VALUES ('11'::int8,'1'::int8),('13'::int8,'2'::int8),('14'::int8,'4'::int8)) v(id,user_id)",
  [['11', '1'], ['13', '2'], ['14', '4']],
  'Сравнивайте дату в пределах своего пользователя; сохраните все максимальные совпадения и порядок групп '
  'user_id.'),
 ('s10-exists-vs-in',
  'sql.subquery.28',
  'SELECT u.id,u.email FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.id AND '
  "o.status='paid')",
  "SELECT u.id,u.email FROM users u JOIN orders o ON u.id=o.user_id WHERE o.status='paid'",
  "SELECT * FROM (VALUES ('1'::int8,'a@example.com'::text),('2'::int8,'b@example.com'::text)) v(id,email)",
  [['1', 'a@example.com'], ['2', 'b@example.com']],
  'Проверьте paid-условие, связь с текущим пользователем и отсутствие умножения строк.'),
 ('s10-cte',
  'sql.subquery.30',
  "WITH paid_totals AS (SELECT user_id,SUM(total) revenue FROM orders WHERE status='paid' GROUP BY user_id) "
  'SELECT user_id,revenue FROM paid_totals WHERE revenue>=150 ORDER BY user_id',
  "SELECT user_id,SUM(total) revenue FROM orders WHERE status='paid' GROUP BY user_id HAVING SUM(total)>150 "
  'ORDER BY user_id',
  "SELECT * FROM (VALUES ('2'::int8,'250.00'::numeric)) v(user_id,revenue)",
  [['2', '250.00']],
  'Суммируйте только paid, включайте границу 150 и сортируйте по user_id.'),
 ('s10-recursive-cte',
  'sql.subquery.32',
  'WITH RECURSIVE chain AS (SELECT id,manager_id,0 depth FROM users WHERE id=4 UNION ALL SELECT '
  'u.id,u.manager_id,c.depth+1 FROM users u JOIN chain c ON u.id=c.manager_id) SELECT id,depth FROM chain '
  'ORDER BY depth',
  'WITH RECURSIVE c AS (SELECT id,manager_id,0 depth FROM users WHERE id=4 UNION ALL SELECT '
  'u.id,u.manager_id,c.depth+1 FROM users u JOIN c ON u.id=c.manager_id WHERE c.depth<1) SELECT id,depth '
  'FROM c ORDER BY depth',
  "SELECT * FROM (VALUES ('4'::int8,'0'::int4),('2'::int8,'1'::int4),('1'::int8,'2'::int4)) v(id,depth)",
  [['4', '0'], ['2', '1'], ['1', '2']],
  'Нужны все предки вверх, исходная строка на depth=0 и пустой результат без стартового пользователя.'),
 ('s10-case',
  'sql.basic.06',
  "SELECT id, CASE status WHEN 'paid' THEN 'completed' WHEN 'cancelled' THEN 'cancelled' ELSE 'pending' END "
  'AS label FROM orders',
  "SELECT id,CASE status WHEN 'paid' THEN 'completed' WHEN 'cancelled' THEN 'cancelled' END AS label FROM "
  'orders',
  'SELECT * FROM (VALUES '
  "('10'::int8,'completed'::text),('11'::int8,'cancelled'::text),('12'::int8,'completed'::text),('13'::int8,'completed'::text),('14'::int8,'pending'::text)) "
  'v(id,label)',
  [['10', 'completed'], ['11', 'cancelled'], ['12', 'completed'], ['13', 'completed'], ['14', 'pending']],
  'Проверьте все ветки, запасной ELSE и сохранение каждой строки заказа.'),
 ('s10-set-operations',
  'sql.set.50',
  'SELECT country FROM users WHERE active EXCEPT SELECT u.country FROM users u JOIN orders o ON '
  "o.user_id=u.id WHERE o.status='paid' ORDER BY country NULLS LAST",
  'SELECT DISTINCT country FROM users WHERE active AND country NOT IN (SELECT u.country FROM users u JOIN '
  "orders o ON o.user_id=u.id WHERE o.status='paid') ORDER BY country NULLS LAST",
  "SELECT * FROM (VALUES ('GE'::text)) v(country)",
  [['GE']],
  'Сравните множества стран, устраните повторы и учитывайте NULL как одно значение EXCEPT.'),
 ('s10-window-functions',
  'sql.window.37',
  'SELECT id,user_id,total,LAG(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS previous_total '
  'FROM orders ORDER BY user_id,created_at,id',
  'SELECT id,user_id,total,LAG(total) OVER(ORDER BY created_at,id) AS previous_total FROM orders ORDER BY '
  'user_id,created_at,id',
  'SELECT * FROM (VALUES '
  "('10'::int8,'1'::int8,'100.00'::numeric,NULL::numeric),('11'::int8,'1'::int8,'40.00'::numeric,'100.00'::numeric),('12'::int8,'2'::int8,'200.00'::numeric,NULL::numeric),('13'::int8,'2'::int8,'50.00'::numeric,'200.00'::numeric),('14'::int8,'4'::int8,'80.00'::numeric,NULL::numeric)) "
  'v(id,user_id,total,previous_total)',
  [['10', '1', '100.00', None],
   ['11', '1', '40.00', '100.00'],
   ['12', '2', '200.00', None],
   ['13', '2', '50.00', '200.00'],
   ['14', '4', '80.00', None]],
  'Окно должно начинаться заново для каждого пользователя; учитывайте id при одинаковых датах и SQL NULL у '
  'первой строки.'),
 ('s10-row-number-rank-dense-rank',
  'sql.window.33',
  'SELECT id,user_id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC,id DESC) AS row_number '
  'FROM orders ORDER BY user_id,row_number',
  'SELECT id,user_id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) AS row_number FROM '
  'orders ORDER BY user_id,row_number',
  'SELECT * FROM (VALUES '
  "('11'::int8,'1'::int8,'1'::int8),('10'::int8,'1'::int8,'2'::int8),('13'::int8,'2'::int8,'1'::int8),('12'::int8,'2'::int8,'2'::int8),('14'::int8,'4'::int8,'1'::int8)) "
  'v(id,user_id,row_number)',
  [['11', '1', '1'], ['10', '1', '2'], ['13', '2', '1'], ['12', '2', '2'], ['14', '4', '1']],
  'Проверьте PARTITION BY, обе сортировки DESC, последовательность без пропусков и итоговый порядок.'),
 ('s10-partition-by-and-window-ordering',
  'sql.window.36',
  'SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS running_total FROM '
  'orders ORDER BY user_id,created_at,id',
  'SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at) AS running_total FROM orders '
  'ORDER BY user_id,created_at,id',
  'SELECT * FROM (VALUES '
  "('10'::int8,'1'::int8,'100.00'::numeric),('11'::int8,'1'::int8,'140.00'::numeric),('12'::int8,'2'::int8,'200.00'::numeric),('13'::int8,'2'::int8,'250.00'::numeric),('14'::int8,'4'::int8,'80.00'::numeric)) "
  'v(id,user_id,running_total)',
  [['10', '1', '100.00'],
   ['11', '1', '140.00'],
   ['12', '2', '200.00'],
   ['13', '2', '250.00'],
   ['14', '4', '80.00']],
  'Проверьте границы partition/frame, хронологический порядок с id и нарастание суммы вместо общего итога.'),
 ('s10-lag-and-lead',
  'sql.window.38',
  'SELECT id,user_id,LEAD(created_at) OVER(PARTITION BY user_id ORDER BY created_at,id) AS next_created_at '
  'FROM orders ORDER BY user_id,created_at,id',
  'SELECT id,user_id,LAG(created_at) OVER(PARTITION BY user_id ORDER BY created_at,id) AS next_created_at '
  'FROM orders ORDER BY user_id,created_at,id',
  'SELECT * FROM (VALUES '
  "('10'::int8,'1'::int8,'2026-02-02T00:00:00Z'::timestamptz),('11'::int8,'1'::int8,NULL::timestamptz),('12'::int8,'2'::int8,'2026-02-04T00:00:00Z'::timestamptz),('13'::int8,'2'::int8,NULL::timestamptz),('14'::int8,'4'::int8,NULL::timestamptz)) "
  'v(id,user_id,next_created_at)',
  [['10', '1', '2026-02-02T00:00:00Z'],
   ['11', '1', None],
   ['12', '2', '2026-02-04T00:00:00Z'],
   ['13', '2', None],
   ['14', '4', None]],
  'Нужна следующая строка своего пользователя с корректным tie-breaker id и SQL NULL на конце.')]
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


def solve_six_case_tasks(tasks=ORDERED_TASKS, earlier_tasks=FILTER_TASKS):
    # Preserve every earlier manifest while completing the next registered group.
    previous = {slug: call(f"/api/sql/lessons/{slug}") for slug in
                [SLUG] + [t[0] for t in earlier_tasks]}
    for index, (slug, task_id, correct, wrong, hardcoded_sql, rows, feedback) in enumerate(tasks):
        lesson_before = call(f"/api/lessons/{slug}")
        assert lesson_before["workspace_kind"] == "sql"
        manifest = call(f"/api/sql/lessons/{slug}")
        assert manifest["task_id"] == task_id and manifest["can_check"] and not manifest["completed"]
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
            if index + 1 < len(tasks):
                assert not call(f"/api/sql/lessons/{tasks[index + 1][0]}")["completed"]
        finally:
            call(path + f"?generation={generation}", method="DELETE", expected=204)
        assert call(f"/api/lessons/{slug}")["files"] == lesson_before["files"]
    for slug, snapshot in previous.items():
        assert call(f"/api/sql/lessons/{slug}") == snapshot
    for slug in [SLUG] + [t[0] for t in earlier_tasks + tasks]:
        assert call(f"/api/sql/lessons/{slug}")["completed"]
    print(f"{[t[0] for t in tasks]} HTTP smoke passed: independent progress; correct 6/6, hardcoded 1/6, ordered Run, safe feedback, replay/conflict, Reset and Explorer isolation; earlier manifests unchanged")


def main():
    if "--sql-offline" in sys.argv:
        assert call("/api/health")["status"] == "ok"
        response = call("/api/sql/sessions", {"lesson_slug": SLUG}, expected=503)
        assert response["error"]["code"] == "runner_unavailable"
        call(CHECK, {"request_id": str(uuid4()), "sql": SOLUTION}, expected=503)
        for slug, task_id, correct, *_ in FILTER_TASKS + ORDERED_TASKS + AGGREGATE_TASKS + JOIN_TASKS + ADVANCED_TASKS:
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
    solve_six_case_tasks()
    solve_six_case_tasks(AGGREGATE_TASKS, FILTER_TASKS + ORDERED_TASKS)
    solve_six_case_tasks(JOIN_TASKS, FILTER_TASKS + ORDERED_TASKS + AGGREGATE_TASKS)
    solve_six_case_tasks(ADVANCED_TASKS, FILTER_TASKS + ORDERED_TASKS + AGGREGATE_TASKS + JOIN_TASKS)
    assert call(f"/api/lessons/{SLUG}")["files"] == original["files"]
    assert call("/api/lessons/is-vs-eq")["files"] == python_before["files"] == python_files
    assert call("/api/lessons/is-vs-eq")["progress"] == python_before["progress"]
    assert call("/api/course")["summary"] == before
    assert check(SOLUTION)["passed"]  # No interactive session required.
    print("SQL Workspace/Check HTTP smoke passed: correct 4/4, hardcoded 1/4, failed/replay/sticky progress, unchanged Explorer; Run/Reset/Close and Python Check/files/progress/XP preserved")


if __name__ == "__main__":
    main()
