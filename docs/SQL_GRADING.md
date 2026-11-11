# SQL Check — Phase 3

One graded task is enabled in lesson **10.2**:
`sql.guided.10.2.projection.v1`, task revision `1`, grader `projection-v1`.
It requires all users, exactly `user_id` (alias of `id`) and `email`, in that
column order. Row order is irrelevant. Existing `sql.basic.01` and the other
48 bank records are unchanged. The bank now has 49 SQL records: 38 legacy
executable references plus this one connected graded task, not 49 integrated labs.

## Execution and ownership

```text
SQL Workspace Check: {request_id, sql}
  → backend lesson/task lookup → short idempotency read (connection closed)
  → runner /v1/check with server-selected revisions
  → global runner admission + one free sandbox slot
  → for each case: create → trusted seed → reference → student → compare → remove
  → bounded safe summary → short SQLite attempt/progress transaction
```

Check does not need an Explorer session. Each case has a fresh PG17 sandbox;
the interactive sandbox, generation and opaque table handles are never used for
grading. Trusted fixture installation runs as OS `postgres`, finishes and closes
its connection before queries start. Reference and student queries both use the
existing OS student UID/peer role, AST allowlist, fresh read-only transaction,
typed executor and resource limits. No arbitrary shell command/path/image/profile
comes from a request. All SQL images and session budgets remain those of Phase 1.

There is one global active runner operation and at most two live sandboxes per
namespace. Check uses one extra slot, sequentially, without a container queue or
eviction. Two active Explorer sessions cause a fail-fast 429. A second backend
Check returns 409 while the first runs. Every grading handle is removed in
`finally`; failed removal retains capacity and is retried by the reaper.
Containers also have a 60-second PID1 watchdog. The workflow deadline is 60
seconds, checked between bounded operations; the last operation and cleanup can
extend it by their individual deadlines. Backend HTTP timeout is 95 seconds,
browser timeout 120 seconds. Current query/row/output caps apply unchanged.

## Deterministic fixtures

The controller-only bundle is `sql_runner/grading/projection-v1/`. Its manifest
is SHA-256 pinned in `app/grading_content.py`, as are each seed's bytes. Request
IDs/revisions do not become paths: the loader accepts one explicit supported
tuple. A future bundle change requires a new grader revision and pin.

| Case revision | Purpose |
| --- | --- |
| `public-v1` | Original four-user `shop-v1` baseline |
| `extra-users-v1` | Seven users, retaining the baseline and adding different IDs/attributes |
| `changed-users-v1` | Three different users, bigint beyond `2^53`, Unicode/case/empty email |
| `empty-users-v1` | Empty tables; catches fabricated/extra rows while checking column types |

Hidden seeds replace data inside their own disposable clusters. The public
schema/seed and checksum remain unchanged:
`a1de3973eb4a2febc818c026def43716109e7ffde6b0bc46721e11d1b2fa4b97`.
Expected rows are computed by the pinned reference query on each fixture, not
copied from the public result. Hidden files and reference SQL are copied only
into the controller image, never the frontend, backend manifest or student image.
This open-source repository contains the fixtures; “hidden” means unavailable
through student runtime/API, not secret from someone reading the repository.

## Comparator and safe feedback

`app/comparator.py` compares column names/order and typed complete results.
Unordered mode uses `Counter` bags, preserving duplicate multiplicities. Ordered
mode compares row sequences. SQL NULL, empty text, literal `NULL`, whitespace,
case and booleans remain distinct. Integer/bigint/numeric strings become Python
`Decimal` without a float/JavaScript Number conversion. Integer/numeric compatibility
is explicitly enabled for this task. Float is a separate exact family with no
tolerance. Empty results still require the right names and type families.

Unsupported types or malformed reference/wire results are infrastructure errors.
Student SQL errors, statement/external timeouts and truncated/oversized results
cannot pass. The current limits are 500 rows, 1 MiB output and 64 KiB per cell;
fixtures have at most seven rows. Larger future tasks need a separate reviewed
grader result budget, rather than accepting an incomplete prefix.

The runner returns only task/revision/checksum, counts, pass flag and up to four
safe feedback codes/SQLSTATE. It discards PostgreSQL messages/details/hints/
positions because even primary cast-error text can contain hidden values. The
backend validates identity and coherent counts, then maps an allowlist of codes
to its own Russian messages. No hidden rows, case identifiers, seeds, reference,
Docker IDs or diagnostics enter the public Check response. Normal public Run
retains PostgreSQL diagnostics. Crash/configuration/transport/cleanup failures
return a sanitized service error and do not create a passing attempt.

## Progress and drafts

`SqlAttempt` and `SqlTaskProgress` are additive tables, separate from
`Attempt`, `LessonProgress` and `UserState`. The principal remains fixed `local`.
Normal passed/failed checks store task/lesson/revisions/checksum, SQL SHA-256 and
the safe result, not the SQL text or hidden values. Infrastructure failures are
retryable and do not persist a grading result. No SQLite transaction spans HTTP.

`(owner, request_id)` is unique. Replaying the same UUID/task/revision/SQL hash
returns the stored grade; reusing it for another query gives 409. A replay also
reports the current sticky completion. Successful progress upserts preserve
`first_passed_at`; failures never remove success. SQL Check makes no changes to
Python saved files, completion, attempts or XP. Course completion/rewards are
deliberately not inferred from this SQL-only state.

Drafts remain browser-local. The new task key imports the Phase 2 guided draft
when absent, retaining the old key. Reset, expiry, theme and Learn/Review do not
clear the SQL text. The lesson's solution is available only after opening its
explicit disclosure; entering Learn/Review closes disclosures. Run displays
results, Check displays Passed/Failed/counts, and only passed Check persists
«Задача решена». Shortcuts are Ctrl/Cmd+Enter and Ctrl/Cmd+Shift+Enter respectively.

## Verification

Use the project's dev environment (the local run used `sql_runner/.venv/bin/python`):

```sh
python3 -m pytest
python3 tools/validate_content.py
cd frontend
npm run test
npm run lint
npx tsc --noEmit
npm run build
cd ..
SQL_TEST_PYTHON=sql_runner/.venv/bin/python scripts/test_sql_runner.sh
SQL_TEST_PYTHON=sql_runner/.venv/bin/python scripts/test_sql_workspace.sh
```

The Docker suites explicitly opt into real PG17 execution; default pytest does
not silently stand in for them. The HTTP stack uses its own namespace and SQLite
tmpfs, never the user's persistence volume. It checks real Python Check before
SQL grading and unchanged files/progress/XP afterward, then verifies SQL outage
does not stop Python Docker Run. The runner suite covers existing privilege,
AST, timeout, resource, lifecycle and Python regression scenarios, plus the
new grader isolation, hidden-value sanitization, hardcoding and crash scenarios.

Additive upgrade has two independent checks:

- A unit test populates all five legacy tables in a legacy-only SQLite file,
  calls `create_all`, records SQL success, then compares every old row exactly.
- Locally, the actual `pythoria_pythoria_data` volume was mounted read-only into
  a networkless temporary helper. Database files were copied to its `/tmp`;
  `create_all` and new SQL-table writes preserved all five legacy table schemas
  and rows exactly. Original file SHA-256 matched before/after. The helper and
  its copy were removed; the original database was not migrated or modified.

Local verification on 2026-11-11 (Docker Engine 28.3.2, PostgreSQL 17.11):
**214 default Python tests, 25 frontend tests and all 35 Docker integration tests
passed** (19 existing execution/security tests plus 16 grading tests). Content
validation, ESLint, TypeScript and production build passed. Both Workspace/Check
HTTP smoke and SQL-outage/Python smoke passed. Test stacks and labeled SQL
sandboxes were removed. One upstream Starlette/AnyIO deprecation warning remains;
content validation reports 279 pre-existing Stage 8+ lessons awaiting quality
review. No manual browser walkthrough was claimed for this phase.

## Adding the next exercise

1. Select a stable task ID tied to the lesson's taught concepts; preserve old IDs.
2. Add an immutable controller bundle: reference, adversarial/edge fixtures, seed
   checksums, columns/types and ordered/bag contract. Register its exact tuple.
3. Extend bank validation and backend capability/task mapping. Do not accept
   client-selected fixture/rule/image fields. Current feedback text for columns
   is specific to this projection task and must become task-aware.
4. Add comparator cases as needed, real restricted-role Docker tests, hardcoded
   public-result rejection and HTTP/frontend regressions. Verify each reference
   is complete within budgets before enabling Check.

This is still a trusted local single-user app with one backend worker/controller
per namespace. Authentication, distributed admission/idempotency, rate limits,
SQL XP, server drafts, DML, free playground and Stage 11 labs need separate work.
Only this single exercise is enabled; adding bank records alone does not expose
new capabilities.
