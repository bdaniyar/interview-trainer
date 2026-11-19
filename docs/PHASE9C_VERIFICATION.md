# Phase 9C advanced PostgreSQL practice

| Lesson | Exercise | Check environment |
| --- | --- | --- |
| 11.4 Index Mental Model | `pg.index.11.4.expression-v1` | Six PostgreSQL fixtures with normalized email matches |
| 11.5 PostgreSQL B-tree | `pg.index.11.5.workload-v1` | Six fixtures with two workload queries and index inspection |
| 11.6 Composite Indexes | `pg.index.11.6.composite-v1` | Six fixtures varying dates, hotels, ties and IDs |
| 11.7 Selectivity | `pg.index.11.7.partial-v1` | Six fixtures with different distributions of new and archived orders |
| 11.8 EXPLAIN and EXPLAIN ANALYZE | `pg.plan.11.8.analysis-v1` | Six fixtures for real join rows, loops and buffers |
| 11.11 MVCC | `pg.tx.11.11.stock-increment-v1` | Six fixture states with two independent concurrent updates |
| 11.14 Connection Pooling | `py.pool.11.14.lifecycle-v1` | Local FastAPI, SQLAlchemy AsyncEngine and real concurrent HTTP |
| 11.15 Pagination | `pg.plan.11.15.range-v1` | Six fixtures with timestamp bounds, stable ties and large IDs |
| 11.17 Booking Concurrency | `pg.tx.11.17.booking-v1` | Existing six-case booking Check and two-session lab |

The index and plan profile serves disposable PostgreSQL 17 data. Run
shows typed rows, natural plans, actual loops, rows and buffers. Three
samples for the optimized query and its baseline are available for
comparison. A separate controlled plan tests index applicability. Check
compares typed results to an independent Python oracle and evaluates the
index design or access condition. Timing is informational. A hidden
fixture includes the next midnight, and one index stores tied row IDs in
the opposite order. A query can therefore appear correct on the public
dataset while failing a hidden contract.

The stock grader allows only the existing transaction SQL policy. A
trusted observer holds a row lock and uses `pg_blocking_pids` to verify
that both independent updates are waiting. It releases the lock and
checks both typed responses, the final increment and other rows. The
pool project runs FastAPI inside a disposable Compose network and tests
exhaustion, committed success, rollback of a failed request and recovery.
The checker uses an AsyncEngine with one connection and zero overflow.
Its results are local to the project.

The restricted index installer applies approved B-tree definitions using
parsed fields. Student SELECT and EXPLAIN run under a restricted role
within resource, output and statement deadlines. The existing SELECT
and transaction permissions apply to the old tasks. SQL progress uses
the existing idempotent store with distinct task identities. SQL XP
remains disabled.

## Verification entry points

- `scripts/test_index_lab.sh` exercises the dedicated Docker profile.
- `scripts/test_transaction_lab.sh` includes the new stock result and lock checks.
- `scripts/test_index_workspace.sh` covers public bindings, Check replay,
  hidden date boundaries, preserved progress and backend restart.
- `node scripts/smoke_sql_browser.mjs --index-only` covers the index UI
  on the disposable workspace. `--transactions-only` covers A/B.
- `projects/pool_lab/check.sh` runs the standalone exercise.

## Results

- 310 default pytest tests and 83 frontend tests passed. Content validation,
  ESLint, TypeScript and the production build passed.
- The dedicated index profile passed all 18 Docker tests. They cover 36
  correct fixture executions, six rejected designs or queries, buffer
  measurements, estimated plans, restricted database access, midnight
  and tied-order adversaries, and safe SQLSTATE feedback.
- The three targeted stock checks passed. They cover the correct increment
  and two wrong updates on all six fixture states. All use actual
  PostgreSQL lock observations.
- The pool reference passed the real Uvicorn and PostgreSQL check. The
  starter failed at the expected assertion about a checked-out
  connection after the first response.
- The full transaction lab suite passed all 55 tests.
- The disposable HTTP test verified all six manifests, real typed rows and
  repeat plans, the date-boundary adversary, a concurrent stock Check,
  UUID replay and progress after a backend restart. It also verified
  unchanged XP and Python files.
- Chrome verified the index lab at 1720 px and 390 px. It displayed 30
  real rows, an Index Only Scan and buffers, and verified both accepted
  and rejected Check, reload, drafts, Reset, Learn/Review, theme and
  navigation to the pool project.
- Shared SELECT, Python and browser regression runs use the complete final stack.
