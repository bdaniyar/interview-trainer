# SQL Check — Phases 3–5

Five lessons use the same grader, dataset and comparator. Task revision is `1`
for all five; column names/order are exact. 10.2–10.4 compare bags, while 10.5–10.6
compare full ordered sequences using the existing comparator unchanged.

| Lesson | Stable task ID | Grader revision | Columns | Cases |
| --- | --- | --- | --- | ---: |
| 10.2 SELECT/AS | `sql.guided.10.2.projection.v1` | `projection-v1` | `user_id`, `email` | 4 |
| 10.3 WHERE | `sql.basic.01` | `active-users-v1` | `id`, `email` | 5 |
| 10.4 NULL | `sql.basic.03` | `null-country-v1` | `id`, `email` | 5 |
| 10.5 ORDER BY/LIMIT/OFFSET | `sql.basic.04` | `latest-orders-v1` | `id`, `created_at` | 6 |
| 10.6 DISTINCT | `sql.basic.05` | `distinct-countries-v1` | `country` | 6 |

All **49 bank records are byte-for-byte unchanged by Phases 4–5**, including the
supplemental email-domain/date tasks. Only these five capabilities are enabled,
one per lesson. `sql.basic.01` retains its historical bank `lesson_number=10.2`;
the explicit capability registry deliberately enables its unchanged active-user
contract in 10.3, after WHERE is taught. Lesson IDs/slugs and interview IDs stay
stable. No SQL progress schema migration is needed in Phases 4–5.

## Explicit task registries

`backend/app/sql_content.py` contains frozen registrations keyed by stable lesson
ID: task ID, task/grader revisions, dataset/checksum, columns, comparison, case
count, starter, prompt and concise task-aware feedback. Duplicate lessons/tasks
are rejected. Bank contracts are validated before projecting a public manifest.
Student requests cannot choose any of these fields.

`sql_runner/app/grading_content.py` contains the separate execution allowlist:
task ID → exact task/grader revisions, fixed bundle directory and SHA-256 pin.
It rejects duplicate task IDs and wrong revisions, and validates manifest identity,
comparison/types, case IDs, seed checksums and filenames. No request value becomes
a filesystem path. The controller validates all reference queries against the
existing AST policy at startup. Content validation stays stdlib-only; explicit
tests verify parity between backend registrations, bank contracts and bundles.

These registries separate lesson/UI capabilities from privileged execution
configuration. Adding a task means adding data registrations and a pinned bundle,
not adding branches to the grader. Missing/corrupt configuration fails closed.

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

Controller-only bundles live in `sql_runner/grading/`. Each manifest is SHA-256
pinned in the execution registry, and each seed is pinned by its manifest.
The loader accepts only registered revision tuples. A future bundle change
requires a new grader revision and pin. The projection bundle is unchanged.

| Case revision | Purpose |
| --- | --- |
| `public-v1` | Original four-user `shop-v1` baseline |
| `extra-users-v1` | Seven users, retaining the baseline and adding different IDs/attributes |
| `changed-users-v1` | Three different users, bigint beyond `2^53`, Unicode/case/empty email |
| `empty-users-v1` | Empty tables; catches fabricated/extra rows while checking column types |

`active-users-v1` uses public baseline (3 matches), `mixed-v1` (4 matches in 7
users, different IDs/emails/insertion order including bigint >2^53),
`all-active-v1` (3 matches), `none-active-v1` (0 matches in 3 users), and
`empty-v1` (0 users). No extra restrictions on syntactically different but
equivalent boolean predicates are imposed: the required result is what matters.

`null-country-v1` uses public baseline (1 match), `multiple-null-v1` (3 matches
in 6 users), `no-null-v1` (0 matches in 3 users), `shifted-null-v1` (1 match with
different IDs/NULL placement) and `empty-v1`. Hidden known-country values include
empty string and literal text `NULL`. Thus `= NULL`, `= ''`, `= 'NULL'` and
baseline-ID hardcoding cannot pass. Fixture cardinalities and every fenced SQL
example from the three lessons are checked against real PostgreSQL.

`latest-orders-v1` has **one public + five hidden cases**: baseline (IDs 14/13),
`scrambled-v1` (unrelated dates/IDs/insertion order, latest orders from different
users), `adversarial-ties-v1` (three equal latest instants crossing LIMIT 2),
`single-v1` (one bigint >2^53 with microseconds/offset), `empty-orders-v1` and
`instants-v1` (equal instants written with different timezone offsets and a
one-microsecond boundary). Reference is the unchanged basic.04 bank query.

The tie case does not depend on accidental heap order. Its pinned trusted seed
adds a private B-tree `(created_at DESC, id ASC)` and sets the disposable student
role's planner preference `enable_seqscan=off`. A test-only EXPLAIN as the exact
student OS/PG role asserts a forward index scan on that index: date-only sorting
then returns IDs 11/12, while the required total order returns 21/12. Repeated
executions verify the distinction. This preference changes neither privileges
nor time/memory limits. The index/configuration exists only inside that case;
public shop-v1, Run and Explorer are unchanged. No EXPLAIN/student DDL capability
or SQL text-matching rule was added. Ordinal ORDER BY/FETCH FIRST and other
semantically equivalent restricted SELECTs can pass.

`distinct-countries-v1` also has **one public + five hidden cases**: baseline,
`mixed-v1` (duplicates, multiple NULLs, empty string, literal text NULL, unsorted
insertion), `all-same-v1`, `null-only-v1`, `changed-v1` and `empty-v1`. The pinned
cluster uses `initdb --locale=C`; fixtures use ASCII uppercase country codes,
and tests assert `pg_database.datcollate/datctype=C`, the libc provider and exact ordered values. Empty string stays in
the result, SQL NULL does not. NULL-only data also distinguishes replacing NULL
with empty string from excluding it. The reference is basic.05's unchanged
query; its historically ambiguous bank word «непустые» is explicitly clarified
as «not SQL NULL» in the lesson/public prompt without rewriting the bank record.

All 20 fenced SQL examples in the new lessons (including disclosed solutions)
execute against real public shop-v1. Tests compare their exact typed rows to
independently declared expectations, verifying the prose's described results.

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
is explicitly enabled for these tasks. Float is a separate exact family with no
tolerance. Empty results still require the right names and type families.

Unsupported types or malformed reference/wire results are infrastructure errors.
Student SQL errors, statement/external timeouts and truncated/oversized results
cannot pass. The current limits are 500 rows, 1 MiB output and 64 KiB per cell;
current reference results have at most seven rows. Larger future tasks need a separate reviewed
grader result budget, rather than accepting an incomplete prefix.

The runner returns only task/revision/checksum, counts, pass flag and up to four
safe feedback codes/SQLSTATE. It discards PostgreSQL messages/details/hints/
positions because even primary cast-error text can contain hidden values. The
backend validates identity and coherent counts, then maps an allowlist of codes
to its own Russian messages. Column feedback uses the registered column names;
row feedback distinguishes projection, filtering, unknown-value, ordering/LIMIT
and uniqueness mistakes.
Messages do not reveal the complete query. With more than four distinct failure
diagnostics, feedback is capped while counts still include every case.
No hidden rows, case identifiers, seeds, reference,
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

Drafts remain browser-local, keyed by stable lesson/task IDs. The projection key imports the Phase 2 guided draft
when absent, retaining the old key. Reset, expiry, theme and Learn/Review do not
clear the SQL text. The lesson's solution is available only after opening its
explicit disclosure; entering Learn/Review closes disclosures. Run displays
results, Check displays Passed/Failed/counts, and only passed Check persists
«Задача решена». Shortcuts are Ctrl/Cmd+Enter and Ctrl/Cmd+Shift+Enter respectively.
Changing lesson remounts the workspace state, discards stale result/feedback and
loads that task's draft/completion. Pending bounded work and Close finish before
the next lesson provisions its session, avoiding the runner's global busy race.
Late replies from the previous lesson cannot change the new lesson's state.

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

Phase 4 verification on **2026-11-13**: **236 default Python tests, 29 frontend
tests and 58 Docker integration tests passed**. The Docker suite includes all
35 previous tests plus 23 WHERE/NULL, fixture-cardinality and lesson-example
tests. After the bounded-feedback adjustment, the three isolation/Reset/fixture
tests were rerun against the final grader and passed. Content validation,
ESLint, TypeScript and production build passed. The real HTTP smoke solves all
three tasks (4/4, 5/5, 5/5), rejects hardcoded public rows (1/4, 1/5, 1/5), checks
task-aware feedback, replay/conflicts and independent completion/Reset, and
confirms unchanged Python Check/files/progress/XP. SQL-controller outage returns
safe errors while Python Docker Run remains available.

An additional temporary networkless helper mounted the actual user volume
read-only, copied SQLite to `/tmp`, ran `create_all` and the actual `record()`
transactions for the two new tasks. Every pre-existing table schema and row
(five legacy tables in this database) matched, and original SHA-256 was unchanged.
Unit tests separately verify existing Phase 3 SQL attempt/progress rows remain
identical while new tasks are completed. There are no model/schema changes in
Phase 4. The two rewritten lesson/interview bundles are marked curated and
removed from legacy debt, leaving 277 pending legacy lessons. Interview IDs
remain the same four positional IDs (`<slug>:0`/`:1`). The upstream AnyIO warning
remains. UI validation uses component tests; no manual browser walkthrough is
claimed.

Phase 5 verification on **2026-11-14**: **238 default Python tests, 32 frontend
tests, content validation, ESLint, TypeScript and production build passed**.
All **58 existing Docker regression scenarios** passed. The full 74-test run
identified one error in the new locale inspection test: PostgreSQL 17 has no
`SHOW lc_collate` GUC. The assertion now reads database collation/provider from
`pg_database` using trusted bootstrap access, without changing student grants.
The entire corrected **16-test ORDER/DISTINCT Docker file was rerun and passed**;
all 74 distinct Docker scenarios are therefore verified. Correct/equivalent SQL
passes 6/6, hardcoded baseline literals pass only 1/6. Adversarial checks cover
tie-breaking, directions, row/column order, LIMIT/OFFSET, duplicates, NULL/empty
string, bigint/timestamp precision, truncation, timeouts and cleanup.

The real Workspace HTTP smoke solves all five lessons, verifies independent
durable completion/replay/failed retries/Reset, ordered public Run results and
unchanged Explorer. During SQL-controller outage, real Python Docker Run **and
Check** still pass with unchanged saved files and no repeat XP. The stack uses
SQLite tmpfs and was removed. No test/helper SQL sandbox remains after cleanup;
an independently started production namespace is left intact.

The actual user SQLite volume was mounted read-only for before/after SHA-256
fingerprints. A networkless temporary helper additionally copied it to `/tmp`
and ran `create_all` plus real `record()` writes for both new tasks; every old
schema/row was preserved on the copy, which was deleted with the helper. Unit
tests preserve exact SQL attempt/progress rows for all three earlier tasks.
Bank records, shop-v1, earlier bundle files/pins, AST policy, comparator and
persistence models are unchanged. No application migration was added. Two
lesson/interview bundles are now curated, leaving 275 legacy lessons outside
scope. The upstream AnyIO warning remains; no manual browser walkthrough is
claimed.

The whole-run source fingerprint **did change**: a separate normal `pythoria`
stack started during verification and has an active production SQL session.
Therefore this phase does not claim that a live user's database stayed byte-for-
byte identical over the entire run. Our test stack never mounts that volume;
all helper mounts of the original are read-only, and all progress-write probes
use disposable copies. The copy's exact-row preservation and isolated HTTP/unit
checks establish SQL progress compatibility without writing to production. No
production services/sessions were stopped or reset.

## Adding the next exercise

1. Select a stable task ID tied to the lesson's taught concepts; preserve old IDs.
2. Add an immutable controller bundle: reference, adversarial/edge fixtures, seed
   checksums, columns/types and ordered/bag contract. Register its exact tuple.
3. Extend bank validation and backend capability/task mapping. Do not accept
   client-selected fixture/rule/image fields. Configure task-aware row feedback;
   column feedback is derived from the registered contract.
4. Add comparator cases as needed, real restricted-role Docker tests, hardcoded
   public-result rejection and HTTP/frontend regressions. Verify each reference
   is complete within budgets before enabling Check.

This is still a trusted local single-user app with one backend worker/controller
per namespace. Authentication, distributed admission/idempotency, rate limits,
SQL XP, server drafts, DML, free playground and Stage 11 labs need separate work.
Only the five listed exercises are enabled; adding bank records alone does not
expose new capabilities. Phase 6 can register aggregation/GROUP BY/HAVING tasks
with their own pinned bundles, empty-group/NULL fixtures, result types and
ordering contracts. This PR does not enable aggregation or JOIN labs.
