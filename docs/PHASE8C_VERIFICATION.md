# Phase 8C verification

Built on Phase 8B commit `e6fa72ae598a88d5774b6b42f8bf8ec9a094e68c`, PR #12.
The independent review boundary contains Stage 20 and its separate training project.
PR #12 was subsequently merged externally as
`98d9969ed68d5636e5f18b1fdd368984017d275b`; its tree is identical to the tested
Phase 8B base. Phase 8C can therefore target main directly.

## Delivered learning scope

All twelve Stage 20 identities have curated Russian notes, concrete practice,
failure mechanisms, interview answers and primary-source references. Five formerly
planned lessons (20.6, 20.9–20.12) are published with executable practice. Totals:
366 published / 406 taxonomy / 68 Python tasks; 242 older lessons remain editorial
debt and are not represented as reviewed.

Five new standard Python exercises cover response-before-BackgroundTasks effect,
capped backoff/validation, canonical request hashing, periodic keys and stale lease
ownership. Their 62 test cases passed in the existing four-second, 128 MiB,
networkless Docker Runner; incomplete starters passed 0/62. The Runner itself and
its dependencies/privileges were not changed.

The five new tasks use opaque parameter IDs and lesson-local report hooks: failing
Check output retains the test name/status and a contract hint without pytest source
frames or captured fixture values. Assertions and outcomes are unchanged. Real HTTP
checks verified both 62/62 references and 0/62 starters, replay XP=0, failed-retry
stickiness, two-file persistence and a relative +100 XP only in disposable test data.
The report hook uses the documented [pytest report API](https://docs.pytest.org/en/stable/reference/reference.html#pytest.hookspec.pytest_runtest_makereport)
and `TestReport.longrepr/sections` (verified 2026-11-17). It does not introduce a new
security boundary between submitted Python and pytest inside the existing sandbox.

The dedicated advanced section in 20.12 explains atomic SKIP LOCKED claiming,
leases, heartbeat, generation/fencing, expiry, stale owners, cancellation, transaction
boundaries and shutdown. Its small Python predicate is explicitly a model; real
database atomicity is checked in the project.

## Real project evidence

- Supported `scripts/test_durable_queue.sh`: 24 passed using PG 17.11, real FastAPI
  HTTP and independent worker processes. Covers simultaneous claims, process death
  after claim/during work, stale return, delayed heartbeat, retry exhaustion,
  cancel/finish race, duplicate HTTP/message, timeout after receiver COMMIT,
  `pg_terminate_backend`, job/outbox rollback and relay recovery, periodic duplicate
  schedules, role restrictions, SIGTERM finishing current work without another
  claim, separation of API/scheduler key namespaces, and two recoverable failures
  followed by success on the final allowed attempt with exactly one local effect.
- Supported `scripts/test_queue_brokers.sh`: actual Redis Lists operations, Celery
  worker/result 385, RabbitMQ publisher confirm/unacked redelivery/DLX/ack, and
  Kafka replay of two records in one partition by two independent consumer groups.
  Tested servers: Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0; Celery 5.5.3.
- `check_restart.py`: a fresh named-volume dev project survived container/PG
  recreation with its queued job intact; replay kept its UUID; two workers produced
  result 55, one local effect and a delivered outbox event. Only the fresh test
  volume, networks and loopback port were used and removed.

The first broker setup exposed wrong Alpine RabbitMQ tmpfs ownership and incomplete
KRaft configuration. These were fixed before the supported successful run. Kafka's
lightweight TCP readiness check avoids repeatedly starting a full CLI JVM; actual
protocol/topic/producer/consumer assertions still run with their own bounded CLI heap.

## Compatibility checks already executed

| Check | Actual result |
| --- | --- |
| Default repository pytest | 288 passed, one existing upstream warning |
| Content validation | Passed, including answer visibility and publication gates |
| Frontend tests | 83 passed |
| Frontend lint / TypeScript / production build | Passed |
| Existing transaction profile integrations | 44 passed |
| Existing SELECT Docker integration suite | 216 passed in one complete invocation (54m43s) |
| Complete supported SQL Workspace HTTP script | Passed: all 23 SQL tasks, outage checks and all five new Python tasks |
| Complete headless Chrome scenario | Passed: 23 SQL tasks, two CLI notes, five Python tasks, themes, shortcuts, drafts and SQL/Python round trips |

A consistent disposable copy of the actual main SQLite database was opened with
the new five capabilities. Every old schema and row, all files, XP and SQL progress
were unchanged. The source volume was mounted read-only; only the container-local
copy received new lesson-progress rows. Seeded API tests separately preserve legacy
completed/theory state and learner drafts when these lessons acquire coding tasks.

The initial HTTP run reached 22 of 23 tasks before the final Check returned
`503 runner_unavailable` while another full Docker suite was active. The diagnostic
cleanup now prints service logs on failure. No timeout or resource limit was relaxed
to hide the failure.

The subsequent full 23-task HTTP block and SQL-outage/Python block passed. Its newly
appended worker smoke failed at the first task's replay assertion without enough
response detail to diagnose that attempt; the assertion now includes the response.
A fresh standalone five-task run passed completely, including replay, with the same
four-second Runner limit. The final complete `scripts/test_sql_workspace.sh` invocation
then passed all 23 SQL tasks, deliberate SQL outage with real Python Run/Check, and
all five new tasks including replay, diagnostic privacy and preserved state.

The first Chrome run passed all 23 SQL tasks and the two transaction notes, then
exposed a harness issue: CDP multiline insertion caused Python reindentation. The
harness now sends each line through native input, supplies Enter's text event and
checks every intermediate prefix without `setValue`/`executeEdits`. A focused real
Chrome run passed all five tasks and 62 cases with preserved companion files.
The [official CDP Input schema](https://github.com/ChromeDevTools/devtools-protocol/blob/master/pdl/domains/Input.pdl)
was checked on 2026-11-17. The final complete browser scenario passed with this
helper, five correct Python Checks, +100 Python XP and no SQL XP. Desktop 1720px and
mobile 390px captures were inspected. The final mobile capture waits for the sidebar
transition to finish; SQL results expose at least two full rows. Companion files and
the last worker draft survive the SQL/Python round trip.

## Main deployment and data preservation

`docker compose -p pythoria up -d --build --wait` completed successfully. The main
frontend, backend and Python Runner are healthy; all 23 SQL manifests are available
and every registered pinned bundle validates in the SQL controller. The catalog
reports 366 published lessons. The two sandbox image-build helpers exited normally.

Consistent SQLite snapshots were taken through a read-only mount of
`pythoria_pythoria_data`, before and after the rebuild. Both schema/row fingerprints
are `ed4aab410c06523f9f78ae212705a8863b58e80adad91b768a939c4bc1cc8e08`.
No production Run/Check was executed and no data was restored. New project tests use
their own tmpfs/namespaces; restart probes remove only their freshly owned volumes.

## Limits

This is a local educational project. Networked PostgreSQL/brokers are separate
from student Python execution. The sample receiver is a durable idempotent ledger,
not a real email/payment provider. The local DB effect shares its transaction with
job completion; arbitrary external effects have no exactly-once guarantee. The
outbox receiver boundary is a separate HTTP/DB transaction, even in the same app.
Periodic backfill, production authentication, cluster failover, operator retry UI,
retention and a full observability deployment remain extensions. The job retry
budget is bounded; the simple outbox relay retains pending intent and retries its
lease until delivery. No SQL XP or application-data migration was introduced.
