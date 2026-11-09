import json
from pathlib import Path

import pytest

from sql_runner.app.datasets import load_dataset, validate_bank
from sql_runner.app.policy import PolicyError, validate

ROOT = Path(__file__).resolve().parents[3]
BANK = json.loads((ROOT / "content/practice_banks.json").read_text())

BANNED = [
    "SELECT 1; SELECT 2", "INSERT INTO users VALUES (1)",
    "UPDATE users SET active=false", "DELETE FROM users", "TRUNCATE users",
    "DROP TABLE users", "ALTER TABLE users ADD x int", "CREATE TABLE t(x int)",
    "CREATE FUNCTION f() RETURNS int LANGUAGE sql AS 'SELECT 1'",
    "CREATE EXTENSION dblink", "GRANT ALL ON users TO student", "SET ROLE postgres",
    "RESET ALL", "DO $$ BEGIN NULL; END $$", "COPY users TO PROGRAM 'id'",
    "SELECT * INTO copied FROM users", "SELECT * FROM users FOR UPDATE",
    "WITH x AS (DELETE FROM users RETURNING *) SELECT * FROM x",
    "SELECT (WITH x AS (UPDATE users SET active=false RETURNING id) SELECT id FROM x)",
    "SELECT * FROM pg_catalog.pg_authid", "SELECT * FROM pg_class",
    "SELECT * FROM information_schema.tables", "SELECT * FROM other.users",
    "SELECT * FROM otherdb.lab.users", "SELECT * FROM sqlite_master",
    "SELECT pg_sleep(1)", "SELECT pg_catalog.pg_sleep(1)",
    "SELECT set_config('statement_timeout','0',false)",
    "SELECT pg_read_file('/etc/passwd')", "SELECT pg_ls_dir('/')",
    "SELECT pg_terminate_backend(1)", "SELECT pg_advisory_lock(1)",
    "SELECT dblink('host=example.com','SELECT 1')", "SELECT lo_import('/etc/passwd')",
    "SELECT current_user", "SELECT 'pg_authid'::regclass", "SELECT * FROM users WHERE xmin > 1",
    "SELECT * FROM users ORDER BY id USING OPERATOR(pg_catalog.<)",
    "SELECT 1 OPERATOR(other.+) 2", "SELECT public.lower('A')", "SELECT custom_function(1)",
    "SELECT pg_catalog.int8(1)", "SELECT pg_catalog.nameeq('a','a')", "SELECT format_type(20,-1)",
    "WITH x AS (SELECT * FROM pg_class), pg_class AS (SELECT 1) SELECT * FROM x",
    "SELECT (WITH pg_class AS (SELECT 1) SELECT * FROM pg_class) FROM pg_class",
    "WITH pg_class AS (SELECT 1) SELECT * FROM pg_catalog.pg_class",
    'SELECT "PG_SLEEP"(1)', "SELECT ARRAY[1,2]", "SELECT 'x'::text[]",
    "EXPLAIN SELECT * FROM users", "BEGIN", "SELECT $1",
]


@pytest.mark.parametrize("query", BANNED)
def test_policy_rejects_unsupported_capabilities_recursively(query):
    with pytest.raises(PolicyError):
        validate(query)


@pytest.mark.parametrize("task", [t for t in BANK["sql"] if t["solution_sql"]], ids=lambda t: t["id"])
def test_existing_reference_subset(task):
    validate(task["solution_sql"])


@pytest.mark.parametrize("query", [
    "SELECT '; DELETE' AS text -- DROP TABLE users\n;",
    'SELECT "email", NULL, true, \'\' FROM "lab"."users"',
    "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)",
    "WITH pg_class AS (SELECT id FROM users) SELECT * FROM pg_class",
    "WITH x AS (SELECT id FROM users), y AS (SELECT * FROM x) SELECT * FROM y",
    "SELECT pg_catalog.lower('A'), 9007199254740993::bigint, 1.234::numeric",
    "SELECT g FROM generate_series(1, 1000) AS g",
    "SELECT coalesce(country, ''), CASE WHEN active THEN 'yes' ELSE 'no' END FROM users",
    "SELECT 1 UNION ALL SELECT 2",
])
def test_reviewed_select_subset(query):
    validate(query)


@pytest.mark.parametrize("query", ["", "  ", "SELECT '\x00'", "SELECT '\ud800'", "SELECT '" + "я" * 17000 + "'"])
def test_byte_budget_and_empty_query(query):
    with pytest.raises(PolicyError):
        validate(query)


def test_parser_syntax_position_in_characters():
    query = "SELECT 'я', FROM users"
    with pytest.raises(PolicyError) as caught:
        validate(query)
    assert caught.value.sqlstate == "42601"
    assert caught.value.position == query.index("FROM") + 1


def test_dataset_revision_and_all_bank_copies_match():
    data = load_dataset()
    assert len(data.checksum) == 64
    validate_bank(BANK)
    with pytest.raises(ValueError):
        load_dataset("../../etc")
    altered = {"sql": [dict(BANK["sql"][0], seed="SELECT 1")]}
    with pytest.raises(ValueError, match="differs"):
        validate_bank(altered)


def test_modified_manifest_cannot_silently_revise_shop_v1(tmp_path, monkeypatch):
    import hashlib
    from sql_runner.app import datasets
    target = tmp_path / "shop-v1"
    target.mkdir()
    original = datasets.load_dataset()
    schema, seed = original.schema.encode(), (original.seed + "\n").encode()
    (target / "schema.sql").write_bytes(schema)
    (target / "seed.sql").write_bytes(seed)
    (target / "manifest.json").write_text(json.dumps({
        "id": "shop-v1", "revision": 1, "postgres_major": 17,
        "checksum": hashlib.sha256(schema + b"\0" + seed).hexdigest(),
        "schema_sha256": hashlib.sha256(schema).hexdigest(),
        "seed_sha256": hashlib.sha256(seed).hexdigest(),
    }))
    monkeypatch.setattr(datasets, "RESOURCE_ROOT", tmp_path)
    with pytest.raises(ValueError, match="new revision"):
        datasets.load_dataset()


def test_ast_complexity_budget():
    with pytest.raises(PolicyError) as caught:
        validate("SELECT " + "(SELECT " * 60 + "1" + ")" * 60)
    assert caught.value.code == "sql_complexity"
