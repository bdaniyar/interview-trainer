# SQL Check — Phases 3–8A

Twenty-three consecutive lessons (10.2–10.24) reuse the same dataset, grader
and typed comparator. All task revisions are `1`; exact columns are mandatory.
The twelve Phase 7 capabilities retain every field and bundle pin. Phase 8A adds
11 six-case bundles. Only `sql.subquery.31` uses ordered groups by `user_id`:
tied latest timestamps retain every order, while order within a user is free.
All other ordered tasks still compare full sequences; unordered tasks compare bags.

| Lesson | Stable task ID | Grader revision | Columns | Cases |
| --- | --- | --- | --- | ---: |
| 10.2 SELECT/AS | `sql.guided.10.2.projection.v1` | `projection-v1` | `user_id`, `email` | 4 |
| 10.3 WHERE | `sql.basic.01` | `active-users-v1` | `id`, `email` | 5 |
| 10.4 NULL | `sql.basic.03` | `null-country-v1` | `id`, `email` | 5 |
| 10.5 ORDER BY/LIMIT/OFFSET | `sql.basic.04` | `latest-orders-v1` | `id`, `created_at` | 6 |
| 10.6 DISTINCT | `sql.basic.05` | `distinct-countries-v1` | `country` | 6 |
| 10.7 Aggregates | `sql.aggregation.09` | `count-orders-v1` | `orders_count` | 6 |
| 10.8 GROUP BY | `sql.aggregation.10` | `orders-by-status-v1` | `status`, `count` | 6 |
| 10.9 HAVING | `sql.aggregation.13` | `users-with-two-orders-v1` | `user_id`, `count` | 6 |
| 10.10 INNER JOIN | `sql.join.17` | `join-order-users-v1` | `order_id`, `email` | 6 |
| 10.11 LEFT JOIN | `sql.join.18` | `users-without-orders-v1` | `id`, `email` | 6 |
| 10.12 RIGHT/FULL OUTER JOIN | `sql.join.25` | `right-join-products-v1` | `product_id`, `order_id` | 6 |
| 10.13 SELF JOIN | `sql.join.20` | `users-managers-v1` | `email`, `manager_email` | 6 |
| 10.14 subqueries | `sql.subquery.27` | `above-average-v1` | `id`, `total` | 6 |
| 10.15 correlated-subquery | `sql.subquery.31` | `latest-per-user-v1` | `id`, `user_id` | 6 |
| 10.16 exists-vs-in | `sql.subquery.28` | `paid-buyers-v1` | `id`, `email` | 6 |
| 10.17 cte | `sql.subquery.30` | `paid-revenue-v1` | `user_id`, `revenue` | 6 |
| 10.18 recursive-cte | `sql.subquery.32` | `manager-chain-v1` | `id`, `depth` | 6 |
| 10.19 case | `sql.basic.06` | `status-label-v1` | `id`, `label` | 6 |
| 10.20 set-operations | `sql.set.50` | `active-countries-except-paid-v1` | `country` | 6 |
| 10.21 window-functions | `sql.window.37` | `previous-total-v1` | `id`, `user_id`, `total`, `previous_total` | 6 |
| 10.22 row-number-rank-dense-rank | `sql.window.33` | `order-row-number-v1` | `id`, `user_id`, `row_number` | 6 |
| 10.23 partition-by-and-window-ordering | `sql.window.36` | `running-revenue-v1` | `id`, `user_id`, `running_total` | 6 |
| 10.24 lag-and-lead | `sql.window.38` | `next-order-time-v1` | `id`, `user_id`, `next_created_at` | 6 |

All **49 pre-existing bank records remain field-identical**; Phase 8A adds only
`sql.set.50` for countries of active users EXCEPT countries of paid buyers.
NULL is a set value, and sorting is country ASC NULLS LAST. The complete bank now
contains 50 records. Explicit capabilities preserve historical lesson numbers:
`basic.01` → 10.3, `subquery.32` (legacy 10.17) → 10.18, `window.38` (legacy 10.21)
→ 10.24. No old task or lesson identity is rewritten. No persistence migration or
SQL XP is introduced. Lesson 10.25 requires the separate Phase 8B write profile.

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
not adding per-task SQL text matching to the grader. Missing/corrupt configuration fails closed.

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

Phase 6 adds three more immutable bundles, each **one public + five hidden cases**:

- `count-orders-v1`: empty, exactly one, seven orders for one user, mixed statuses,
  sparse IDs and differing user/order counts. Empty input returns one row containing
  bigint zero. Counting users, grouping by ID or returning public literal 5 fails.
- `orders-by-status-v1`: empty, a single status, skewed/equal group counts and
  shuffled insertion/ownership. Tests assert complete columns and ordered groups;
  wrong keys, filtered or missing groups, incorrect counts and missing/reverse order fail.
- `users-with-two-orders-v1`: empty, no qualifying users, 1/2/3 boundary, multiple
  qualifying users (including bigint ID beyond 2^53), and a single qualifying user.
  Users without orders exist in the fixtures. Both two and three qualify; `> 2`,
  `= 2`, including single orders, wrong counts and reverse order fail.

Seeds use proper user/order foreign keys and only existing `paid`, `new`,
`cancelled` statuses; at most ten orders. Independent tests assert all 18 case
outputs, rather than merely checking reference execution. Every correct reference,
`COUNT(id)` variant and permitted equivalent grouped CTE passes 6/6; hardcoded public
results pass only 1/6. No literal HAVING/text matching is enforced. These are new
registrations, not a CTE lesson or expanded SELECT policy.

All **30 SQL blocks** in the three curated lessons run against public PG17:
28 successful examples have independently specified exact results, and two clearly
marked invalid examples must produce SQLSTATE 42803. Tests cover empty/all-NULL
aggregates, COUNT(column)/DISTINCT, SUM/AVG/MIN/MAX, bigint/numeric type metadata and
exact high-precision values. No comparator change or numerical tolerance was needed.
Bank exercises `.11`, `.12`, `.14`, `.15`, `.16` remain supplemental without Check.
Solutions and complete interview answers stay closed in Learn and Review.

Phase 7 adds four immutable bundles, each **one public + five hidden cases**:

- `join-order-users-v1`: empty orders, repeated ownership, crossed primary IDs,
  bigint order IDs above 2^53, shuffled inserts and users without orders. Unordered
  comparison retains every order, including repeated owner emails.
- `users-without-orders-v1`: mixed 0/1/many orders, everyone ordered, nobody
  ordered, empty users/orders and large/nonsequential IDs. A nullable country is
  deliberately unrelated to order absence. NOT EXISTS and checks of another
  right-side NOT NULL key remain valid equivalents.
- `right-join-products-v1`: unsold products, multiple orders per product, all
  unsold, empty products, a real order ID zero, shuffled/bigint IDs and exact
  product/order ordering. The public data has no unsold products, so INNER JOIN
  coincides there and on the empty case, but fails the complete Check (2/6).
- `users-managers-v1`: roots, a multi-level hierarchy, several roots, one user,
  no users and several employees sharing a manager. Parent rows are inserted
  before dependent rows and all self-FKs remain valid. Only the immediate manager
  is requested; the original user's ID determines ordering.

All 24 reference outputs have independent typed golden rows. Wrong keys,
Cartesian products, missing/unmatched/extra rows, reversed relations and ordering,
wrong aliases, NULL-to-zero/text substitutions and baseline hardcoding are tested.
Every reference and equivalent comma/WHERE, NOT EXISTS, swapped LEFT/RIGHT or
RIGHT self-join solution passes 6/6; public constants pass only 1/6.

**DISTINCT nuance:** order IDs, full product/order pairs and user emails are
unique under the schema. Full-row DISTINCT may be equivalent and is accepted.
DISTINCT ON a product/manager alone can suppress required relationships and is
rejected. Bag comparison also rejects extra copies of an otherwise correct row;
it never reduces output to a set of emails or product IDs.

**FULL/FK limitation:** with full unfiltered users/orders and the exact PK/FK
condition, NOT NULL `orders.user_id` prevents orders without users. Bank task
`sql.join.26` therefore cannot evaluate both unmatched sides. The 10.12 Check is
only `sql.join.25`. Teaching and dedicated PG17 tests use independent VALUES
relations: left-only key 1, matching key 2, right-only key 3, explicit ORDER BY and
NULL-extended typed columns. The INNER/LEFT/RIGHT/FULL variants return 1/2/2/3 rows.
No FK, schema, AST allowlist, student privilege or container limit is relaxed.

The four curated Russian lessons contain **43 executable SQL blocks**. Independently
specified column names, PG types, row values and sequences/bags are asserted:
41 successful examples and two clearly marked ambiguous-column errors (42702).
LEFT JOIN's substantive ON/WHERE comparison verifies 5/3/4 rows, including the
case that `WHERE paid OR id IS NULL` still loses a user with only a new order.
The ON-filter task `.21`, FULL task `.26` and other bank exercises stay ungraded.
Reference solutions and full interview answers remain closed in Learn and Review.

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
current reference results have at most eight rows. Larger future tasks need a separate reviewed
grader result budget, rather than accepting an incomplete prefix.

The runner returns only task/revision/checksum, counts, pass flag and up to four
safe feedback codes/SQLSTATE. It discards PostgreSQL messages/details/hints/
positions because even primary cast-error text can contain hidden values. The
backend validates identity and coherent counts, then maps an allowlist of codes
to its own Russian messages. Column feedback uses the registered column names;
row feedback distinguishes projection, filtering, unknown-value, ordering/LIMIT,
uniqueness, aggregate source, group counts, HAVING boundaries, join relationships,
missing matches, retained products and manager direction mistakes.
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

## Phase 6 verification — 2026-11-14

**240 default Python tests, 37 frontend tests and the complete 98-test real Docker
suite passed**, together with content validation, ESLint, TypeScript and the
production build. All 24 new aggregation Docker scenarios passed in the full run.
The existing upstream Starlette/AnyIO deprecation warning remains.

The real HTTP smoke completed all eight tasks independently. New references
score 6/6, baseline hardcoding 1/6; wrong-source/group/order/threshold submissions
fail. Run leaves completion false, successful Check persists, failed retries do
not clear it, UUID replay is idempotent and changed SQL with the same UUID returns
409. Reset and grading leave Explorer unchanged. Earlier SQL manifests and Python
files/progress/XP compare equal before and after the new tasks. During SQL-controller
outage, all eight Check routes return sanitized 503 and real Python Docker Run
**and Check** continue to pass with the same files and no repeat XP.

Grading tests use unique namespaces; HTTP tests use the disposable tmpfs stack.
A separate networkless helper opened the real user volume read-only and used
SQLite's backup API for a consistent disposable copy. Actual `create_all` and
`record()`/replay calls for all three new tasks preserved every pre-existing schema
and row across all seven tables. Seeded regressions also preserve exact attempt
and progress rows for the previous five SQL tasks. No persistence schema, XP rule
or migration was changed. No production service/session was stopped for tests.

The bank's 49 SQL entries, shop-v1 schema/seed/checksum, previous five bundles and
SHA pins, grader, comparator, AST policy and persistence implementation are
unchanged. Three lesson/interview bundles are curated, leaving 272 legacy lessons
outside this phase; lesson IDs/slugs and the six positional interview IDs remain
stable. All 30 new lesson SQL blocks have independently verified PG17 results,
including two deliberately invalid examples checked as SQLSTATE 42803.

Headless Chrome also traversed **10.2 → 10.9** against a fresh disposable stack:
real Monaco, public Run/results and independent saved drafts in every lesson;
6/6 Check in all three new lessons via Cmd+Shift+Enter, with Cmd+Enter Run;
closed reference disclosures, theme switching and draft restoration on returning
to GROUP BY. Desktop **1720×1050** keeps editor/results together; mobile
**390×844** switches to the Results tab, hides the sidebar after its transition
and has no horizontal page overflow. Stable desktop/light/mobile screenshots
were inspected. The browser profile and test stack were removed afterwards.

After verification, the user-authorized main **`pythoria`** project was rebuilt
with `docker compose -p pythoria up -d --build --wait`. Frontend, backend and both
runners passed health probes; all eight public manifests expose the expected task
and `can_check=true`, and the running SQL controller validates all eight bundles.
Consistent read-only SQLite backups before/after deployment have identical logical
fingerprints: every schema and row is preserved. This update is a deployment,
separate from test execution; the named volume was retained. Test stacks/profiles
were removed and no labeled test/grade SQL containers remain.

## Phase 7 verification — 2026-11-15

**242 default Python tests and 48 frontend tests passed**, along with content
validation, ESLint, TypeScript and the production build. The four JOIN lessons and
eight positional interview records are curated; 268 older lessons remain outside
this phase's review scope. Lesson IDs/slugs, question IDs and priority/set metadata
are preserved. No AI-track planning files are changed.

**The complete 132-test Docker suite passed in one run**, including all 98
previous scenarios and all 34 new JOIN/content scenarios. The existing
Starlette/AnyIO deprecation warning remains; no test was skipped.
All 34 new JOIN/content scenarios cover references/equivalents at 6/6, public
hardcoding at 1/6, correct and incorrect join keys/types, row multiplicity,
column aliases/order, NULL versus text/zero, bigint IDs, timeouts/truncation,
safe errors, unchanged Explorer and cleanup. An INNER JOIN in the RIGHT task
coincides on public/all-sold and empty-product data but scores only 2/6 overall.
No grading/query policy or comparator change was needed.

All **43 lesson SQL blocks** have independently authored names, PG types, row
values and ordered/bag expectations: 41 successful examples plus two expected
42702 errors. The independent VALUES FULL example additionally verifies INNER,
LEFT, RIGHT and FULL outputs, including both unmatched sides. FK-constrained
users/orders is explicitly not advertised as a complete two-sided FULL test.

A networkless helper mounted the actual user volume read-only and used SQLite's
backup API for a consistent disposable copy. Real `create_all`, `record`, UUID
replay and failed-retry writes for the four new tasks preserved every original
schema and row across all seven tables. Seeded backend regressions separately
preserve exact attempts/progress for all eight previously completed SQL tasks.
No destructive migration, model change or SQL XP was introduced.

An AST-based source comparison verifies that every field of the previous eight
backend/runner registrations is identical, including prompts, starters, case
counts and SHA pins. Git comparison protects all eight bundle directories,
49 SQL bank entries, shop-v1 schema/seed/checksum, grader/comparator/AST policy,
persistence implementation and AI curriculum plan.

The real HTTP smoke passed across all 12 lessons using the disposable stack:
public typed Run results and columns, Run not completing tasks, wrong/correct
Check, baseline hardcoding, sticky completion, UUID replay/conflict, Reset and
Explorer isolation. All earlier eight manifests and Python files/progress/XP
compare equal before and after the four new tasks. Stopping only the test SQL
controller returns sanitized 503 on all 12 Check routes while real Python Docker
Run **and Check** still pass with unchanged files and no repeat XP. The tmpfs
stack and test sandboxes were removed; production data is never mounted by it.

Post-run screenshot review exposed a mobile-only layout issue: the longer self-join
prompt plus Check feedback left almost no visible table body. A narrow CSS rule
allocates 75% of the vertical split to the SQL pane only in mobile Results view;
Editor and desktop layouts retain their existing behavior. After this UI-only
change, all 48 frontend tests, ESLint, TypeScript and production build were rerun
and passed. The SQL/backend code and all files read by the full 132-test Docker
suite remained unchanged. The committed `scripts/smoke_sql_browser.mjs` adds a
real browser regression requiring at least two complete visible mobile rows.

The final committed Chrome walkthrough passed on a fresh disposable stack after
that CSS change: all 12 lessons accepted actual Monaco typing, public Run and
correct Check (4/4, 5/5 or 6/6 according to the existing contracts). All four new
reference disclosures stayed closed in Learn and Review. Theme changes updated
Monaco, Explorer showed the self-referencing FK, and drafts/completion remained
independent. A real Python editor change survived SQL → Python → SQL navigation;
the second Python file stayed byte-identical and SQL awarded no XP. Desktop
1720×1050 and mobile 390×844 screenshots were inspected, with visible result rows
and no horizontal overflow. Only explicit pre-execution busy responses receive
bounded retries in the browser helper; failed grading and SQL errors fail the
walkthrough. The private browser profile and tmpfs stack were removed afterwards.

After testing, the main `pythoria` project was rebuilt under the user's standing
instruction to update it after every phase, separately from the isolated tests.
`docker compose -p pythoria up -d --build --wait` retained the named data volume.
Frontend, backend and both runners passed health checks; all 12 public manifests
expose the expected task and Check capability, and the running SQL controller
validates all 12 registered bundles. Consistent read-only SQLite backups before
and after deployment have the same logical SHA-256 fingerprint: every schema and
row is preserved. No labeled test/grading SQL containers remain.

## Phase 8A verification — 2026-11-16

Eleven advanced SELECT lessons (10.14–10.24) are curated, including publication
of the existing recursive-CTE and LAG/LEAD identities. There are 361 published
lessons, 259 remaining legacy reviews and still 406 taxonomy IDs. All existing
question positions, lesson IDs/slugs, priorities and prerequisites are preserved.
The read-only bank has 50 records: the previous 49 are field-identical, and only
`sql.set.50` is added. Every previous registration field and bundle pin is checked
against a committed Phase 7 snapshot.

**251 default Python tests, 81 frontend tests**, content validation, ESLint,
TypeScript and production build passed. Real HTTP smoke passed all 23 tasks:
Run versus Check, correct/wrong/hardcoded results, replay/conflict, sticky progress,
Reset, earlier manifests, unchanged Explorer and Python files/progress/XP. All
23 Check routes return sanitized errors on test SQL-controller outage while
real Python Docker Run and Check remain available.

The initial complete 216-test Docker invocation produced **215 passes and one
failure in a new test expectation**, not a runner change: recursive materialization
hit the existing temporary-file budget (53400) before statement timeout. The
corrected test separately proves resource exhaustion, a CPU-bound recursive
57014 deadline, sandbox disposal and recovery through a fresh session. The whole
**84-test advanced SELECT file was rerun and passed**; the other **132 existing
Docker tests passed unchanged** in the original invocation. This records the
actual runs rather than claiming a second complete 216-test invocation.

All 66 new fixture outputs have independently calculated typed expectations.
References and equivalent subquery/join/EXISTS/window formulations pass 6/6;
public hardcoding passes only 1/6. Wrong global/group averages, missing correlation,
latest-date ties, duplicate-producing joins, strict revenue boundaries, truncated
manager chains, missing CASE ELSE, NULL-sensitive anti-sets, absent window
partitions/tie-breakers and wrong frames/neighbour directions fail.

All **43 lesson SQL blocks** were executed on the pinned PG17 sandbox: 42
successful results with independent names/types/rows and one deliberate 21000
cardinality error. Recursive fixtures are acyclic as promised by the immutable
legacy reference; cycle-safe synthetic teaching and nontermination/resource tests
are separate. No function/schema/AST privilege was added. The comparator's new
optional ordered-key groups apply only to `sql.subquery.31`; legacy default bag
and full-sequence comparisons remain unchanged.

Headless Chrome passed actual Monaco typing and Run/Check across **all 23 lessons**,
Learn/Review answer closure, independent drafts/completion, shortcuts, themes and
Explorer relationships. Inspected screenshots cover 1720×1050 desktop and 390×844
mobile with visible result rows and no horizontal page overflow. A SQL → Python
editor change → SQL round trip preserved both Python files and the SQL draft;
all SQL checks awarded zero XP. The private browser profile and tmpfs stack were
removed afterwards.

A networkless helper mounted the real user volume read-only, took a consistent
SQLite backup, and performed actual success, UUID replay and failed-retry progress
writes for all eleven new tasks on the disposable copy. Every pre-existing schema
and row in all seven tables survived. Backend regressions separately seed and
preserve exact attempts/progress for all twelve previous SQL tasks. The live
volume is never mounted by the test stack. No AI-track planning files changed.

After verification the user's standing per-phase update instruction was applied:
the main `pythoria` project was rebuilt with `up -d --build --wait`, separately
from tests. Frontend, backend and both runners passed health checks, all 23
public task manifests expose Check, and the running controller validates every
registered bundle. Consistent read-only SQLite backups before/after deployment
have identical logical schema/row fingerprints; the named data volume is retained.

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
Only the 23 listed exercises are enabled; adding bank records alone does not
expose new capabilities. Phase 8A covers the remaining advanced SELECT lessons. Writable DML and actual
multi-connection transaction labs require a separate execution profile in Phase 8B;
server drafts and SQL XP remain separate work. No AI-track planning files are changed by these SQL implementation phases.
