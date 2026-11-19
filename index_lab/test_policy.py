import pytest

from index_lab.policy import indexes, plan_submission
from index_lab.workloads import PLAN_SQL
from sql_runner.app.policy import PolicyError


@pytest.mark.parametrize("query", [
    "DROP INDEX anything",
    "CREATE INDEX x ON pg_catalog.pg_class (relname)",
    "CREATE INDEX x ON q.orders (id)",
    "CREATE UNIQUE INDEX x ON orders (user_id)",
    "CREATE INDEX CONCURRENTLY x ON orders (user_id)",
    "CREATE INDEX x ON orders USING hash (id)",
    "CREATE INDEX x ON orders (id) WITH (fillfactor = 10)",
    "CREATE INDEX x ON orders (id) TABLESPACE pg_global",
    "CREATE INDEX x ON users (pg_catalog.upper(email))",
    "CREATE INDEX x ON users (lower(email COLLATE \"C\"))",
    "CREATE INDEX x ON orders (id) WHERE status='new' OR 1=1",
    "CREATE INDEX x ON orders (id) WHERE id IN (SELECT id FROM orders)",
    "CREATE INDEX x ON orders (id); CREATE TABLE more(v integer)",
])
def test_structural_index_admission_rejects_unscoped_mutations(query):
    with pytest.raises(PolicyError):
        indexes(query)


@pytest.mark.parametrize("query", [
    "EXPLAIN (ANALYZE, BUFFERS) DELETE FROM orders",
    "EXPLAIN (ANALYZE, BUFFERS, SETTINGS) SELECT 1",
    "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM pg_catalog.pg_class",
    "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders FOR UPDATE",
    "EXPLAIN SELECT * FROM orders",
    "EXPLAIN (ANALYZE, BUFFERS) WITH changed AS (UPDATE orders SET id = 1 RETURNING *) SELECT * FROM changed",
])
def test_explain_only_executes_reviewed_select_forms(query):
    with pytest.raises(PolicyError):
        plan_submission(query, estimate_allowed=False)


def test_quoted_equivalent_keys_are_canonicalized():
    design = indexes("CREATE INDEX other ON lab.\"orders\" (\"created_at\" DESC, id DESC) WHERE 'new'::text = status")
    assert design[0].active_only
    assert [key.field for key in design[0].keys] == ["created_at", "id"]
    assert all(key.descending for key in design[0].keys)
    statement, analyze = plan_submission(
        "EXPLAIN (ANALYZE, BUFFERS, TIMING OFF) " + PLAN_SQL, estimate_allowed=False
    )
    assert "SELECT" in statement and analyze


def test_plain_explain_is_only_available_in_public_run():
    expected, analyze = plan_submission("EXPLAIN " + PLAN_SQL, estimate_allowed=True)
    assert "SELECT" in expected and not analyze
