# SQL Workspace — Phases 2–8A

Enabled for **10.2–10.24** (23 lessons). The first twelve stable lesson IDs are
`backend-interview.10.2.select-aliases-and-expressions`,
`backend-interview.10.3.where-and-boolean-logic`,
`backend-interview.10.4.null-and-three-valued-logic`,
`backend-interview.10.5.order-by-limit-and-offset`,
`backend-interview.10.6.distinct`, `backend-interview.10.7.aggregates`,
`backend-interview.10.8.group-by`, `backend-interview.10.9.having`,
`backend-interview.10.10.inner-join`, `backend-interview.10.11.left-join`,
`backend-interview.10.12.right-and-full-outer-join` and
`backend-interview.10.13.self-join`. Phase 8A adds all eleven IDs at 10.14–10.24
listed in [SQL_GRADING.md](SQL_GRADING.md), including newly published recursive
CTE and LAG/LEAD. Other lessons keep their
existing workspace. Lesson IDs and Python completion/XP rules are unchanged.
Phase 3 added SQL-only attempt/progress tables; Phases 4–8A reuse them without a
migration. Registry/task details are in [SQL_GRADING.md](SQL_GRADING.md).

## Local use

```sh
docker compose up -d --build --wait
```

Open [lesson 10.2](http://localhost:3000/?lesson=s10-select-aliases-and-expressions).
The same workspace works in [10.3 WHERE](http://localhost:3000/?lesson=s10-where-and-boolean-logic)
and [10.4 NULL](http://localhost:3000/?lesson=s10-null-and-three-valued-logic).
Continue to [10.5 ORDER BY/LIMIT/OFFSET](http://localhost:3000/?lesson=s10-order-by-limit-and-offset)
and [10.6 DISTINCT](http://localhost:3000/?lesson=s10-distinct), then
[10.7 Aggregates](http://localhost:3000/?lesson=s10-aggregates),
[10.8 GROUP BY](http://localhost:3000/?lesson=s10-group-by) and
[10.9 HAVING](http://localhost:3000/?lesson=s10-having), then
[10.10 INNER JOIN](http://localhost:3000/?lesson=s10-inner-join),
[10.11 LEFT JOIN](http://localhost:3000/?lesson=s10-left-join),
[10.12 RIGHT/FULL JOIN](http://localhost:3000/?lesson=s10-right-and-full-outer-join) and
[10.13 SELF JOIN](http://localhost:3000/?lesson=s10-self-join). Continue through
[10.14 subqueries](http://localhost:3000/?lesson=s10-subqueries) to
[10.24 LAG/LEAD](http://localhost:3000/?lesson=s10-lag-and-lead).
SQL Lab opens a `shop-v1` session automatically. Edit `query.sql`, press Run or
Ctrl/Cmd+Enter, inspect real PostgreSQL results. The Database tab shows table
columns, nullable/type metadata, ordered PK and FK pairs, and pages of 50 rows.
FK links select the referenced table, including users' self-reference.

Check (Ctrl/Cmd+Shift+Enter) evaluates four fixture revisions for
`sql.guided.10.2.projection.v1`, five for `sql.basic.01` (WHERE) and five for
`sql.basic.03` (NULL), and six each for `sql.basic.04` (latest orders) and
`sql.basic.05` (distinct countries), plus six each for `sql.aggregation.09`,
`.10` and `.13` (aggregates/GROUP BY/HAVING). The four JOIN tasks `.17`, `.18`,
`.25`, `.20` also have six cases each. Each advanced SELECT task in 10.14–10.24
has one public and five hidden cases. In 10.15, all tied latest orders are retained;
Check enforces user_id group order but allows any order within each group. Lessons 10.5–10.9 and 10.12–10.13 use
ordered comparison; INNER/anti-join (10.10–10.11) compare complete bags of rows. It shows Passed/Failed, counts and task-aware safe
feedback. Run never marks the task solved. Successful Check persists «Задача
решена» independently of Python completion, including after a later failed Check
or reload. SQL Check awards no XP and works without an active Explorer session.

Refresh updates catalog/data. Reset creates a fresh baseline and rotates the
generation/handles, preserving the editor text. Result diagnostics include
SQLSTATE and a clickable editor position; Unicode positions are translated to
Monaco's UTF-16 columns. Query errors/cells are rendered as text. Duplicate
aliases, NULL, empty string, booleans, bigint/numeric and empty results remain
distinct. Truncated results say there are more rows, without inventing a total.

On desktop, editor and results remain together after Run/Check when the SQL pane
is wider than 420px. At viewport widths up to 820px, tabs preserve editing space. In mobile
Results view the SQL pane gets 75% of the split height, so long prompts/Check
feedback leave readable table rows; Editor view retains its existing split.
Learn/Review and theme changes do not create another session or clear the draft.
The task answer is behind an explicit disclosure in the lesson, closed in both
modes. Guided-only capabilities do not render Check.

## Data ownership and persistence

`backend/app/sql_content.py` owns the capability mapping by stable lesson ID.
Its public manifest projects task ID/revision, prompt, starter, expected column
names, Check capability and persisted completion. It never returns reference SQL,
hidden fixtures, expected rows or grader rules.
Only these twelve published lessons get `workspace_kind=sql` in the lesson API.
Each lesson has its own task, draft, result, completion and disposable session.
Navigation waits for pending work/Close before provisioning the next lesson's
session; stale results cannot populate another lesson's workspace.

SQL drafts are stored **only in this browser** under
`pythoria:sql:<stable-lesson-id>:<task-id>`. Phase 2's `guided-select` draft is
copied to the new key if no graded draft exists; the old value is retained.
Each edit is saved synchronously;
Ctrl/Cmd+S also saves locally. Storage errors are displayed without clearing the
editor. SQL never goes to the Python `/files` endpoint. CourseApp saves Python
files against the loaded Python lesson before navigation, and unmounts its Python
workspace/listeners when SQL is active.

The backend holds at most two ephemeral bindings, from a new public opaque ID to
the runner's private session ID, fixed local principal, lesson and generation.
It validates binding/generation before forwarding and rewrites IDs in responses.
Clients cannot choose owner, dataset, image, paths, credentials or budgets. Per
binding admission fails fast on concurrent Run/Reset; the runner still enforces
its global limits independently. Run/Explorer routes never open an SQLite
transaction or execute a database driver. Check uses short SQLite reads/writes,
closed before contacting the grader; submitted SQL only executes in PostgreSQL
sandboxes. Requests use a separate bounded HTTP client, with 35-second
provisioning/reset, 15-second other session calls and 95-second Check timeouts
(browser Check timeout: 120 seconds). The SQL request
body limit is 256 KiB with a separate 32 KiB UTF-8 SQL budget.

Idle expiry is 15 minutes, absolute expiry 30 minutes. Backend cleanup retries
failed closes; runner TTL/startup reaper/watchdog remain independent. Leaving the
lesson closes the session after outstanding operations finish, including a late
create/reset response. Page unload uses best-effort keepalive Close; abrupt
browser/network failure falls back to TTL. Backend restart loses public bindings;
runner restart loses the underlying sessions. The UI keeps the draft and offers
to create another session on expiry/failure. An interrupted create without a
received ID may occupy a runner slot until its TTL; creation is not blindly
retried. Capacity/busy errors explain how to retry.

This remains a trusted local single-user application, one backend worker and one
SQL controller per namespace. Authentication, tenant isolation, server drafts,
durable playground databases, immediate query cancellation and SQL XP belong
to later phases.

## Public backend API

| Endpoint | Contract |
| --- | --- |
| `GET /api/sql/lessons/{slug}` | Public capability/progress manifest; unsupported/unpublished lesson returns 404 |
| `POST /api/sql/lessons/{slug}/tasks/{task_id}/check` | `{request_id: UUID,sql}` → safe grade and sticky `completed`; no session required |
| `POST /api/sql/sessions` | `{lesson_slug}` → public session info, 201 |
| `POST /api/sql/sessions/{id}/run` | `{generation,sql}` → typed result, errors, `session_closed` |
| `GET /api/sql/sessions/{id}/catalog?generation=1` | Table handles and schema metadata |
| `GET /api/sql/sessions/{id}/tables/{handle}/rows?generation=1&limit=50&offset=0` | Default 50 / maximum 100 rows; bounded offset |
| `POST /api/sql/sessions/{id}/reset` | `{generation}` → generation + 1 |
| `DELETE /api/sql/sessions/{id}?generation=1` | Idempotent 204 |

Lifecycle errors use `{error:{code,message}}` with 404/409/410/429/503. Query
errors stay inside the typed result. Internal HTTP errors are sanitized; SQL
validation errors do not echo the submitted payload. Extra fields in requests
are rejected. Raw runner IDs do not resolve through this API. A bad table handle
does not invalidate an otherwise valid session.

The backend uses `SQL_RUNNER_URL=http://sql-runner:8002` inside Compose. The runner
still has no published host port. Existing Python routes remain independent and
work when SQL Runner is unavailable. `FRONTEND_ORIGINS` optionally configures
backend CORS for a separate local preview; defaults stay localhost:3000.

## Verification

```sh
python3 -m pytest
python3 tools/validate_content.py
cd frontend
npm run test
npm run lint
npx tsc --noEmit
npm run build
cd ..
scripts/test_sql_workspace.sh
```

The last command builds/runs `docker-compose.sql-workspace-test.yml`, tests the
real backend → internal SQL API → PostgreSQL chain, then removes only that named
test stack. Its SQLite database lives in tmpfs; the user's `pythoria_data` volume
is never mounted. No `down -v` is used. It covers Run/JOIN/catalog/browse, invalid
handles, SQLSTATE, policy/output limits, Reset/stale generations/Close and
unchanged Python files/progress. It then stops only the test SQL controller and
verifies a sanitized SQL 503 while the backend and real Python Docker Run still
work.

Phase 3 extends this smoke with real Python Check and saved files first, then SQL
correct 4/4, missing alias/columns/rows, duplicate rows, hardcoded public data 1/4,
safe cast errors, idempotent replay and conflict, sticky completion, unchanged
Explorer generation/handles/rows and unchanged Python progress/XP. SQL outage
also verifies Check returns a sanitized 503.

Phase 4 extends the same smoke to solve WHERE/NULL (5/5), reject hardcoded public
rows (1/5), verify task-aware feedback/cross-task rejection, and preserve each
task's independent completion through failed attempts and Reset. It verifies
Python Check, files, progress and XP before/after the three SQL tasks. Component
tests cover 10.2 → 10.3 → 10.4, independent draft restoration, delayed Check/Close,
theme, shortcuts and closed Learn/Review solutions for all three lessons.

Phase 5 extends navigation/disclosure tests to all five lessons and adds real
HTTP solutions for latest orders and distinct countries (6/6 each), ordered
public Run results, incorrect tie/dedup queries, baseline hardcoding (1/6),
independent completion/reload/Reset and unchanged Explorer. During SQL-controller
outage the smoke now verifies both real Python Docker Run **and Check**, keeping
the same saved Python files and awarding no repeat XP. Test SQLite remains tmpfs;
the user's volume is not mounted by the stack.

Phase 6 extends the same navigation/disclosure/late-response tests to all eight
lessons. The real HTTP smoke additionally opens 10.7–10.9, checks public ordered
Run rows and aliases, correct 6/6, wrong queries and hardcoded baseline 1/6,
independent sticky completion, UUID replay/conflict, Reset and unchanged Explorer.
Every earlier SQL manifest and Python files/progress/XP remain unchanged. Outage
checks cover all eight tasks while real Python Run and Check stay operational.
No SQL is sent to Python `/files`; drafts stay in their task-specific browser keys.

Phase 7 extends component navigation and late-reply isolation to **10.2 → 10.13**.
The HTTP smoke completes all four JOIN tasks with real PostgreSQL, correct 6/6,
incorrect Check, hardcoded 1/6, independent/sticky progress, replay/conflict,
Reset and unchanged Explorer/earlier eight manifests. Outage checks include all
12 task routes and real Python Docker Run/Check with preserved files and XP.
The four lesson/interview bundles are curated; answers remain closed in both modes.

10.12's Check preserves every product and position. The supplemental FULL users/
orders query cannot show orders without users under the current FK. A SELECT-only
VALUES example demonstrates both unmatched sides without changing shop-v1 or the
read-only boundary. The ON/WHERE exercise `.21` and FULL `.26` remain ungraded;
no lesson at 10.14 or later is enabled in this phase.

After each implemented phase, the authorized local workflow is to rebuild and
update the main `pythoria` project with `docker compose up -d --build --wait`,
then check frontend, backend and both runners. The named data volume is retained.
A recreated SQL controller ends ephemeral sessions; the workspace can recreate
its session while browser drafts and persistent task completion remain saved.
Tests use only the separate stack and never stop main services for test purposes.

For a repeatable Chrome walkthrough, run this after the HTTP smoke has removed
its stack. It requires a fresh tmpfs DB, Node 22 and Chrome (set
`SQL_TEST_CHROME` to the executable path on another platform):

```sh
docker compose build sandbox sql-sandbox sql-runner
docker compose -f docker-compose.sql-workspace-test.yml up -d --build --wait
# http://localhost:13000/?lesson=s10-select-aliases-and-expressions
node scripts/smoke_sql_browser.mjs
docker compose -f docker-compose.sql-workspace-test.yml down
```

The real PostgreSQL execution/security tests from Phase 1 remain separate:
`scripts/test_sql_runner.sh`. Frontend tests exercise draft persistence, reset,
session cleanup and late responses, StrictMode, shortcuts, typed result/error
rendering, and navigation across Python/SQL without changing saved Python files.

See [SQL_GRADING.md](SQL_GRADING.md) for Phase 3 verification and upgrade evidence.
Browser interaction is covered by component tests and the completed Phase 7
headless Chrome walkthrough at 1720×1050 and 390×844. The committed
`scripts/smoke_sql_browser.mjs` passed all 12 tasks with real Monaco typing,
Run/Check shortcuts, theme changes, draft restoration, visible mobile rows and a
Python file-edit/navigation round trip. A mobile Results-only split adjustment
keeps table rows visible below longer prompts and Check feedback. The separate Docker HTTP smoke exercises
backend/runner/PostgreSQL and Python availability during SQL-controller outage.

Implementation references: [Monaco React](https://github.com/suren-atoyan/monaco-react),
[React effect cleanup](https://react.dev/reference/react/useEffect),
[FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/).

## Phase 8A — advanced SELECT

All 23 lessons from 10.2 through 10.24 now use the established workspace. The
new tasks have six cases each; details and actual verification runs are recorded
in [SQL_GRADING.md](SQL_GRADING.md#phase-8a-verification--2026-11-16).
Recursive CTE and LAG/LEAD were published only with curated notes and real PG17
verification. Historical bank mappings remain explicit rather than rewriting IDs.

The committed Chrome smoke now traverses all 23 lessons with actual Monaco
input, Run/Check, closed answers, themes, desktop/mobile results and SQL/Python
file ownership. The HTTP smoke likewise covers all 23, including SQL outage and
real Python Run/Check. The user data volume is excluded from both stacks.

## Web Transaction Lab

Lessons 10.25 and 11.17 use the dedicated
[Transaction Lab](../transaction_lab/README.md). Two independent connections
share one disposable PostgreSQL database during a live session. The
timeline shows typed results, SQLSTATE and lock waiting reported by
PostgreSQL. Check uses six fresh databases per assignment. It records
attempts and task completion with UUID replay in the existing SQL tables.

The same workspace exposes the controlled exercises for Stage 11. CLI
commands remain available and emit local JSON. The SELECT workspace keeps
its read-only profile and immutable bundles.
