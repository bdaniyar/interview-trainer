# Phase 8B verification

Parent: Phase 8A PR #11, merged into main as
`b6bf55a0ce873e3eb273550b6836c29a9f3d3c6e`.
This delivery does not merge its own PR.

## Delivered scope

- Curated Russian notes and preserved interview identities for 10.25 and
  11.2, 11.6, 11.8–11.13, 11.17. All ten were already published; catalog remains
  361 lessons / 406 taxonomy records / 63 Python tasks. Legacy curation debt: 249.
- Separate `pg-transaction-v1` CLI/image/policy/roles, disposable networkless PG
  17.11 databases, non-superuser SQL, bounded resources and cancellation/TTL.
- Two revision-1 state-and-result checks: `pg.write.10.25.status-v1` and
  `pg.tx.11.17.booking-v1`, six fresh cases each (one public, five hidden).
- Twelve controlled scenarios with real independent A/B connections: RC/RR,
  MVCC, savepoint/rollback, NOWAIT/SKIP LOCKED, blocking UPDATE, deadlock,
  SERIALIZABLE, lost update, plain EXPLAIN and exclusion conflict.

The supported first interface is a local CLI with statement/result timelines.
There is no two-editor web UI, durable SQLite completion for these two checks,
SQL XP or interval-calendar implementation. Index plans are not performance claims.

## Executed checks

| Command | Observed result |
| --- | --- |
| `python3 -m pytest` (repository dev venv) | 283 passed; one existing upstream Starlette/AnyIO deprecation warning |
| `python3 tools/validate_content.py` | Passed, including publication and answer-leak gates |
| Frontend `npm run test` | 83 passed |
| Frontend lint / `tsc --noEmit` / production build | Passed |
| `scripts/test_transaction_lab.sh` | 44 passed on real PostgreSQL |
| `scripts/test_sql_runner.sh` | One complete invocation: 216 passed, one upstream warning, 2366.38 s |

The 44 new-profile integrations include all twelve lesson SQL blocks (eleven
successful results and one expected CHECK violation), twelve controlled timelines,
all six cases for reference/equivalent/unsafe/hardcoded submissions, actual
FK/UNIQUE/CHECK errors, savepoint recovery, open-transaction rollback, direct role
and container restrictions, external cancellation and orphan watchdog cleanup.
Explicit FOR UPDATE and SERIALIZABLE booking variants pass; a DML CTE passes.
State checks preserve all unrelated tables and rows. Check output contains no
hidden fixture values.

The original parallel regression attempt encountered Docker infrastructure timeouts
during large image extraction. It was stopped. The complete sequential 216-test
invocation above is the final regression evidence; sandbox deadlines were unchanged.

## Compatibility and deployment

Source comparison against the parent leaves all 23 SELECT registrations/bundles,
shop-v1, SQL policy/grader/comparator, Python Runner, backend models and AI curriculum
plan unchanged. The old twelve registrations and original bank records remain
protected by the inherited exact-contract tests. Transaction Lab does not import
SQLite progress or application models and never mounts the Pythoria volume.

Full HTTP smoke passed all 23 SQL tasks, wrong/correct/hardcoded checks, replay,
Reset, independent sticky progress and earlier manifests. With SQL Runner stopped,
all 23 routes returned sanitized 503 while real Python Docker Run/Check, files,
progress and XP stayed available.

Headless Chrome passed all 23 with native Monaco input, Run/Check, theme,
desktop/mobile layouts, two complete mobile result rows, drafts and SQL/Python
round trip preserving both Python files. Both new CLI-graded lesson references
remain closed in Learn and Review. Desktop/mobile screenshots were inspected.

Main `pythoria` was rebuilt after verification under the standing per-phase update
instruction. Frontend/backend/Python health and all 23 SQL manifests passed; the
controller validated every pinned bundle. Consistent SQLite snapshots were taken
with the main volume mounted read-only. Before/after deployment logical SHA-256:
`ed4aab410c06523f9f78ae212705a8863b58e80adad91b768a939c4bc1cc8e08`.
Every previous schema and row was preserved; no test writes to the main volume.
