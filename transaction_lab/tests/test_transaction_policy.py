import pytest
from transaction_lab.policy import validate_script
from sql_runner.app.policy import PolicyError, validate
from transaction_lab.control import DML_REFERENCE, BOOKING_REFERENCE


@pytest.mark.parametrize(
    "source",
    [
        DML_REFERENCE,
        BOOKING_REFERENCE,
        "BEGIN ISOLATION LEVEL SERIALIZABLE; SELECT id FROM inventory FOR UPDATE NOWAIT; ROLLBACK;",
        "BEGIN; SAVEPOINT s; UPDATE inventory SET available=0 WHERE id=1; ROLLBACK TO SAVEPOINT s; COMMIT;",
        "INSERT INTO orders(id,user_id,status,total,created_at) VALUES(90,1,'new',3,'2026-01-01') ON CONFLICT(id) DO UPDATE SET status=excluded.status RETURNING id",
        "EXPLAIN SELECT * FROM orders WHERE user_id=1",
    ],
)
def test_separate_profile_admits_only_its_intended_capabilities(source):
    validate_script(source)


@pytest.mark.parametrize(
    "source",
    [
        "CREATE TABLE x(id integer)",
        "DROP TABLE orders",
        "TRUNCATE orders",
        "ALTER ROLE student SUPERUSER",
        "SET ROLE postgres",
        "RESET ROLE",
        "SET statement_timeout=0",
        "COPY orders TO PROGRAM 'id'",
        "SELECT pg_read_file('/etc/passwd')",
        "SELECT pg_blocking_pids(1)",
        "SELECT * FROM pg_catalog.pg_roles",
        "SELECT * FROM public.orders",
        "SELECT * FROM other.lab.orders",
        "UPDATE users SET active=false",
        "WITH x AS (DELETE FROM users RETURNING *) SELECT * FROM x",
        "SELECT * INTO x FROM orders",
        "PREPARE TRANSACTION 'x'",
        "COMMIT PREPARED 'x'",
        "EXPLAIN DELETE FROM orders",
        "EXPLAIN (ANALYZE) DELETE FROM orders",
        "SELECT lo_import('/etc/passwd')",
        "SELECT * FROM pg_ls_dir('/')",
        "SELECT 1; " * 17,
    ],
)
def test_profile_rejects_admin_shell_schema_and_unbounded_capabilities(source):
    with pytest.raises(PolicyError):
        validate_script(source)


@pytest.mark.parametrize(
    "source", [DML_REFERENCE, BOOKING_REFERENCE, "SELECT id FROM orders FOR UPDATE"]
)
def test_existing_select_profile_stays_read_only(source):
    with pytest.raises(PolicyError):
        validate(source)
