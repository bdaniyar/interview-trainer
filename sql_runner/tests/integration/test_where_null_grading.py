import json
from pathlib import Path
import re

import pytest

from sql_runner.app.grader import check
from sql_runner.app.grading_content import REGISTRY, load_task

WHERE = "SELECT id,email FROM users WHERE active IS TRUE"
NULL = "SELECT id,email FROM users WHERE country IS NULL"


def grade(manager, task_id, sql):
    entry = REGISTRY[task_id]
    return check(manager, task_id, entry.task_revision, entry.grader_revision, sql)


@pytest.mark.parametrize("task_id,sql", [
    ("sql.basic.01", WHERE + " ORDER BY id DESC"),
    ("sql.basic.01", "select u.id, u.email from lab.users u where u.active = true"),
    ("sql.basic.01", "SELECT id,email FROM users WHERE active"),
    ("sql.basic.03", NULL + " ORDER BY email DESC"),
    ("sql.basic.03", "select u.id,u.email from lab.users u where not (u.country is not null)"),
])
def test_equivalent_where_and_null_queries_pass_all_five_cases(manager, task_id, sql):
    result = grade(manager, task_id, sql)
    assert result["passed"] and result["tests_passed"] == result["tests_total"] == 5
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,sql", [
    ("sql.basic.01", "SELECT id,email FROM users"),
    ("sql.basic.01", "SELECT id,email FROM users WHERE NOT active"),
    ("sql.basic.01", "SELECT email,id FROM users WHERE active"),
    ("sql.basic.01", WHERE + " LIMIT 1"),
    ("sql.basic.01", WHERE + " UNION ALL " + WHERE),
    ("sql.basic.03", "SELECT id,email FROM users WHERE country = NULL"),
    ("sql.basic.03", "SELECT id,email FROM users WHERE country = ''"),
    ("sql.basic.03", "SELECT id,email FROM users WHERE country = 'NULL'"),
    ("sql.basic.03", "SELECT id,email FROM users WHERE country IS NOT NULL"),
    ("sql.basic.03", "SELECT id AS user_id,email FROM users WHERE country IS NULL"),
    ("sql.basic.03", NULL + " LIMIT 1"),
    ("sql.basic.03", NULL + " UNION ALL " + NULL),
])
def test_wrong_predicates_columns_missing_and_duplicate_rows_fail(manager, task_id, sql):
    result = grade(manager, task_id, sql)
    assert not result["passed"] and result["tests_passed"] < result["tests_total"]
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,sql", [
    ("sql.basic.01", "SELECT * FROM (VALUES (1::bigint,'a@example.com'),(2::bigint,'b@example.com'),(4::bigint,'d@example.com')) t(id,email)"),
    ("sql.basic.03", "SELECT 3::bigint AS id,'c@example.com' AS email"),
])
def test_hardcoded_public_results_pass_only_baseline(manager, task_id, sql):
    result = grade(manager, task_id, sql)
    assert not result["passed"] and result["tests_passed"] == 1 and result["tests_total"] == 5
    assert not manager.backend.containers()


@pytest.mark.parametrize("task_id,sql", [("sql.basic.01", WHERE), ("sql.basic.03", NULL)])
def test_check_isolation_safe_feedback_policy_and_reset(manager, session, task_id, sql):
    sid = session["session_id"]
    before = manager.run(sid, 1, "SELECT * FROM users ORDER BY id")
    catalog = manager.catalog(sid, 1)
    assert grade(manager, task_id, sql)["passed"]
    assert manager.catalog(sid, 1) == catalog
    assert manager.run(sid, 1, "SELECT * FROM users ORDER BY id")["rows"] == before["rows"]
    result = grade(manager, task_id, "SELECT id,email::bigint AS email FROM users")
    wire = json.dumps(result)
    assert not result["passed"] and result["feedback"][0]["sqlstate"] == "22P02"
    assert "@example" not in wire and "reference_sql" not in wire and "seed" not in wire
    for query in ["DELETE FROM users", "CREATE TABLE hacked(x int)", "SELECT 1; SELECT 2"]:
        assert grade(manager, task_id, query)["feedback"][0]["code"] == "policy"
    assert len(manager.backend.containers()) == 1
    reset = manager.reset(sid, 1)
    assert manager.run(sid, reset["generation"], "SELECT * FROM users ORDER BY id")["rows"] == before["rows"]
    assert grade(manager, task_id, sql)["passed"]


def test_all_sql_examples_from_three_lessons_execute_on_shared_schema(manager, session):
    root = Path(__file__).resolve().parents[3] / "content/stage-10"
    for slug in ["s10-select-aliases-and-expressions", "s10-where-and-boolean-logic", "s10-null-and-three-valued-logic"]:
        markdown = (root / slug / "lesson.md").read_text()
        queries = re.findall(r"```sql\n(.*?)```", markdown, re.S)
        assert queries
        for query in queries:
            result = manager.run(session["session_id"], 1, query)
            assert result["error"] is None, (slug, query, result["error"])
            assert not result["truncated"]


def test_fixture_references_have_expected_cardinalities(manager):
    # Verify the edge-case design itself, not only student/reference agreement.
    expected = {"sql.basic.01": [3, 4, 3, 0, 0], "sql.basic.03": [1, 3, 0, 1, 0]}
    for task_id, counts in expected.items():
        entry = REGISTRY[task_id]
        task = load_task(task_id, entry.task_revision, entry.grader_revision)
        with manager.admission(), manager.registry:
            for case, count in zip(task.cases, counts):
                handle = manager.backend.create("fixture-proof-" + case.id, 1, lifetime=60)
                try:
                    if case.seed is not None:
                        manager.backend.install_fixture(handle, case.seed)
                    result = manager.backend.execute(handle, "run", {"sql": task.reference_sql})
                    assert result["error"] is None and result["rows_returned"] == count
                finally:
                    manager.backend.remove(handle)
        assert not manager.backend.containers()
