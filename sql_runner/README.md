# SQL Runner — Phase 1

Independent PostgreSQL 17 execution service for trusted, local, single-user
Pythoria. There is no application backend/UI integration, grading, XP, draft
storage or application database migration in this phase.

## Run

Docker Desktop/Engine with at least another 1 GiB available for two SQL sandboxes:

```sh
docker compose up -d --build --wait sql-runner
docker compose exec sql-runner python -m sql_runner.app.smoke
docker compose logs sql-runner
```

The smoke command creates its own session, calls Run/catalog/browse/Reset and
closes it in `finally`. It does not contact the existing backend. The service
listens on **internal port 8002**, with no host port published. Dynamic sandbox
containers have **no network**, no ports, no bind mounts and no persistent
volumes. No change to Python runner services or `pythoria_data` is needed.

Stop just this controller with `docker compose stop sql-runner`. It closes its
leases gracefully. Never use `down -v` to manage SQL sessions. A controller crash
is covered by the startup/periodic reaper and a separate sandbox PID1 watchdog.

## Trust boundaries

`app/main.py` → `lifecycle.Manager` → `docker_backend.DockerBackend` → disposable
PostgreSQL cluster → fixed `executor.py` using psycopg. The controller has Docker
socket access and is consequently privileged. It mounts no application data or
credentials. Neither its socket nor application files are copied into sandboxes.

The sandbox image pins PostgreSQL **17.11** by digest; pglast **7.22** parses the
PG17 grammar. Its non-root PID1 initializes a cluster in tmpfs as OS `postgres`.
The fixed query executable runs as OS UID **65532**, whose only matching peer
role is **student**. PostgreSQL listens only on a Unix socket. Student cannot
impersonate the bootstrap owner using connection parameters. The student role
has no superuser/createdb/createrole/replication/bypassrls flags, admin memberships,
TEMP/CREATE rights or object ownership. It has CONNECT/USAGE/SELECT on `lab`.

Default PUBLIC execution privileges on pg_catalog functions and SELECT on catalog
tables are revoked. Only reviewed functions and builtin scalar cast/operator
implementations are granted; Explorer gets SELECT
on four metadata catalogs and EXECUTE on `format_type`. Direct catalog relations
and **all** user calls to unapproved functions, including `format_type`, are
still rejected by the AST policy. This limited metadata access is intentional;
database permissions alone do not hide every piece of PostgreSQL metadata.
Every Run uses a fresh read-only connection/transaction which is closed on exit.

This is **not a public multi-user hosting boundary**. There is one fixed trusted
local principal, no authentication, and exactly one controller/uvicorn worker per
namespace. Opaque IDs prevent accidental selection, not unauthorized access.
Public hosting needs authenticated owner binding, rate limits and an isolated
worker host. Do not expose this Docker-privileged API to an untrusted network.

## Dataset

`resources/shop-v1/{schema.sql,seed.sql,manifest.json}` is the canonical revision
copied byte-for-byte from the 38 executable tasks in `practice_banks.json`.
Four users, five orders, three products, five order_items; constraints, precision,
composite PK and users' self FK are preserved. Each session has its own copy.
Both per-file and combined SHA-256 hashes are checked against a code-pinned
digest. A dataset change requires a **new revision**. `validate_content.py` and
unit tests check bank parity. No bank/lesson rewrite is part of this PR.

## SQL capabilities

One SELECT (including VALUES/set operations), expressions, WHERE, JOIN, DISTINCT,
GROUP BY/HAVING, ORDER BY, LIMIT/OFFSET, subqueries/EXISTS, read-only CTEs,
recursive CTEs, CASE/COALESCE, reviewed aggregates/windows. All 38 existing
reference queries are exercised on the restricted role by the Docker suite.

Tables: unqualified shop names or `lab.<table>`, plus lexically visible CTEs.
Functions: count/sum/min/max/avg, lower/upper/length, abs/round/ceil/floor,
row_number/rank/dense_rank, lag/lead/first_value/last_value/nth_value,
repeat/generate_series. Qualification only by `pg_catalog` is accepted.
Scalar casts: boolean, text/varchar/char, integers, numeric, float, date/time,
timestamp (including zones), interval, UUID. Ordinary arithmetic/comparison,
LIKE/ILIKE and concatenation are supported. Unsupported AST nodes fail closed.

Blocked: DML/DDL, writable CTEs, SELECT INTO, row locks, COPY (including PROGRAM),
DO, extensions/functions/procedures, role/privilege/session changes, EXPLAIN,
multiple statements, system/cross-database tables and columns, file/network/admin
functions, arbitrary functions/operators/types, arrays/JSON/composite values,
SEARCH/CYCLE and prepared parameters. This is a conservative teaching subset,
not every valid PostgreSQL SELECT. No regex splitting or appended text LIMIT.

## Internal API

JSON request bodies reject unknown fields. The client cannot supply image,
container ID, credentials, paths, owner, budgets or capability profiles.

| Endpoint | Request | Response |
| --- | --- | --- |
| `GET /health` | — | readiness after startup cleanup |
| `POST /v1/sessions` | `{"dataset_id":"shop-v1"}` or `{}` | 201 session ID, generation, dataset checksum, expiry, cold start |
| `POST /v1/sessions/{id}/run` | `{"generation":1,"sql":"SELECT id,email FROM users"}` | typed SELECT result/error |
| `GET /v1/sessions/{id}/catalog?generation=1` | — | columns/types/nullable, ordered PK/FK pairs, opaque table handles |
| `GET /v1/sessions/{id}/tables/{handle}/rows?generation=1&limit=50&offset=0` | — | bounded result, PK ordering |
| `POST /v1/sessions/{id}/reset` | `{"generation":1}` | new cluster, baseline, generation + 1, new handles |
| `DELETE /v1/sessions/{id}?generation=1` | — | 204, idempotent close |

Browse maximum is 100, offset maximum 10000. Identifiers come from a verified
session/generation-specific handle, then use `psycopg.sql.Identifier`; values use
parameters. FK pairing uses `conkey/confkey` in ordinal order, including composite
and self references. It does not rely on information_schema's FK visibility.

Lifecycle errors: 404 unknown ID/handle, 410 expired/failed/closed, 409 stale
generation or busy operation, 429 capacity, 503 infrastructure failure. Validation
errors are bounded and do not echo the rejected payload. Query/policy errors are
returned in the result's `error` field. PostgreSQL errors expose bounded primary
message, SQLSTATE, safe hint and **one-based character** position in the original
SQL, compensating for the driver's DECLARE wrapper. No traceback/DSN is returned.

Rows use `columns[]` + `rows[][]`, retaining duplicate aliases. All numbers are
strings (including integers and Decimal), with PG type name/OID; bool remains
JSON boolean, SQL NULL is JSON null, empty string remains empty. Date/time use
ISO 8601, timestamptz is normalized to UTC `Z`; interval is Python timedelta's
text and UUID is its canonical text. Float uses Python's round-trip text;
nonfinite numeric/float values are textual, never invalid JSON numbers.
Types outside this scalar set produce a structured resource error.

## Budgets and failure handling

| Resource | Limit |
| --- | --- |
| SQL | 32 KiB UTF-8; one statement; AST 2000 nodes/depth 50 |
| HTTP body | 256 KiB, including escaped JSON text; independent SQL byte limit |
| PG statement / lock / idle transaction / transaction | 2 s / 500 ms / 2 s / 5 s |
| External query / provisioning deadline | 5 s / approximately 20 s, plus bounded Docker RPC/cleanup time |
| Results | 500 rows + one lookahead; 1 MiB JSON; 64 KiB/cell; 128 columns |
| Sandbox | 512 MiB RAM, no swap, 1 CPU, 128 PIDs, dropped caps, no-new-privileges |
| Writable storage | PGDATA tmpfs 256 MiB, socket 1 MiB, temp 8 MiB, shadowed image VOLUME 1 MiB |
| PG | 10 connections; shared_buffers 32 MiB; work_mem 4 MiB; temp_file_limit 32 MiB; no parallel workers/JIT |
| Admission | 2 sessions; 1 active operation globally, fail fast instead of queueing |
| Lease | idle 15 min, absolute 30 min; reaper every 30 s |

The named psycopg **ServerCursor** fetches one row at a time and stops after one
lookahead or byte cap. `has_more/truncated` never claims a total count. An oversized
cell returns an error rather than an altered cell value. The executor runs inside
the memory-constrained container, so even decoding an extreme single value cannot
allocate it in the controller. Large sorts/aggregates still need time/memory caps.

An external watchdog kills the actual container on deadline, with at most one
outstanding Docker exec future and no unbounded queue. PostgreSQL execution
timeouts/resource failures and crashes close the lease. Ordinary SQL/output
errors roll back and leave the immutable session usable. Reset is serialized
against Run; it removes the old cluster before provisioning a replacement. It
does not extend the lease's absolute lifetime. Failed cleanup retains capacity
until the reaper succeeds. Tombstones are capped at 128.

Every sandbox is labeled by controller namespace and session. Startup discards
that namespace's previous leases; periodic cleanup retries orphan removals. A
PID1 alarm enforces an independent maximum 30-minute container lifetime even if
the controller is killed. Containers auto-remove on exit. No background process
depends on the HTTP client remaining connected: a disconnected request finishes
within the query budget; immediate user cancellation is a later API extension.

## Tests

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest                         # no Docker/PG required
.venv/bin/python tools/validate_content.py
SQL_TEST_PYTHON=.venv/bin/python scripts/test_sql_runner.sh -s
```

The last command builds both SQL images and the existing Python sandbox for its
regression test, then explicitly opts into real PostgreSQL
integration tests. Running that directory without `SQL_DOCKER_TESTS=1` skips it.
Tests use unique namespaces and remove only their own containers. They cover the
reference corpus, direct privilege/peer-auth bypass attempts, catalog composite
FK/self FK, bounded output, statement/lock/idle/external timeouts, two-session
isolation, Run/Reset races, reset/expiry/restart/watchdog/crash cleanup and the
existing Python Docker Run/Check/terminal. Default unit tests use fake Docker
backends and deterministic clocks/events. `SQL_BENCHMARK` prints measured cold
start and cgroup memory usage (including tmpfs, not a production RSS/SLO promise).

Implementation references: [Psycopg cursor storage and bounded retrieval](https://www.psycopg.org/psycopg3/docs/advanced/cursors.html),
[PostgreSQL 17 privileges](https://www.postgresql.org/docs/17/sql-grant.html),
[PostgreSQL 17 transaction/statement timeouts](https://www.postgresql.org/docs/17/runtime-config-client.html).

Verified locally on 2026-11-09: Docker Engine 28.3.2 / Linux aarch64 (Docker
Desktop), PostgreSQL 17.11; **160 default tests and 19 Docker integration tests
passed**. The Compose HTTP smoke also passed. A cached-image sandbox took
589 ms to initialize in the benchmark; Compose smoke samples took 0.8–1.3 s.
Cgroup usage was 96,075,776 bytes (~92 MiB), including tmpfs, with 27,435,008
anonymous bytes (~26 MiB). These are small-seed samples, not load/peak-memory
guarantees. No labeled SQL sandboxes remained after tests; application SQLite
file checksums matched before/after. One upstream Starlette/AnyIO deprecation
warning remains in the local dev environment.

Phase 2 can build the backend client and workspace against this typed internal
contract. It must bind sessions to the server's local principal, handle generation
and expiry explicitly, keep SQL drafts separate from Python saved files, and
render cells/errors as text. No SQL Check or XP should be inferred from Run.
