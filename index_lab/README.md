# PostgreSQL Index and Plan Lab

Open lessons 11.4–11.8 or 11.15 in Pythoria to run the appropriate exercise.
Run uses a fresh public dataset. Check verifies the design or query on six
independent datasets and persists task completion. Reset clears the preview
and keeps the SQL draft. The query plan shows estimates, real rows and loops,
buffers and repeated timing samples. Public plain EXPLAIN shows estimates.
Check for the plan lesson requires ANALYZE and BUFFERS.

| Lesson | Task | Grade requirements |
| --- | --- | --- |
| 11.4 | `pg.index.11.4.expression-v1` | B-tree key `lower(email)` and all normalized matches |
| 11.5 | `pg.index.11.5.workload-v1` | Two minimal indexes for two feeds, including one partial index |
| 11.6 | `pg.index.11.6.composite-v1` | Hotel equality, date range and stable ordering |
| 11.7 | `pg.index.11.7.partial-v1` | Active-only predicate, correct rows and index-provided order |
| 11.8 | `pg.plan.11.8.analysis-v1` | Real SELECT output and EXPLAIN ANALYZE with buffer counters |
| 11.15 | `pg.plan.11.15.range-v1` | Right date boundary, exact rows and ordered IDs, both bounds usable |

A separate disposable PostgreSQL image carries synthetic `users` and
`orders`. The student role executes guarded SELECT and EXPLAIN. A trusted
installer validates at most two CREATE INDEX statements, reconstructs the
allowed B-tree definitions from parsed fields and verifies the resulting
catalog objects. It uses known owned relations, bounded key counts and a
fixed partial-index predicate. The process that runs student queries remains
unprivileged. Sandboxes have no network, Docker socket, host mounts or SQLite
access. The existing Docker scheduler supplies per-operation deadlines and a
60-second process watchdog.

Grading compares typed rows against a Python oracle. Independent cases vary
size, distributions, missing results, duplicated normalized emails, tied
timestamps and large IDs. One case has rows at the exclusive midnight
boundary. A controlled EXPLAIN makes sequential access less attractive to
prove that PostgreSQL can use the intended path. Natural plans and timings
remain observable. Timing depends on caches and hardware and is informational.

Additional advanced work is available in 11.11 and 11.14. Check in 11.11
uses two PostgreSQL sessions to increment stock while preserving all other
rows. The local FastAPI project in `projects/pool_lab` tests concurrent HTTP
requests and a real constrained SQLAlchemy pool. The Booking task in 11.17
continues to use its original two-session Check.

Verification entry points are `scripts/test_index_lab.sh`,
`scripts/test_index_workspace.sh` and `scripts/test_transaction_lab.sh`.
Run `node scripts/smoke_sql_browser.mjs --index-only` against the disposable
Compose workspace for the focused Chrome walkthrough.
