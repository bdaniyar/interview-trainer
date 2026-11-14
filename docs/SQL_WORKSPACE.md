# SQL Workspace — Phases 2–5

Enabled for **10.2–10.6**. Their stable lesson IDs are
`backend-interview.10.2.select-aliases-and-expressions`,
`backend-interview.10.3.where-and-boolean-logic` and
`backend-interview.10.4.null-and-three-valued-logic`,
`backend-interview.10.5.order-by-limit-and-offset` and
`backend-interview.10.6.distinct`. Other lessons keep their
existing workspace. Lesson IDs and Python completion/XP rules are unchanged.
Phase 3 added SQL-only attempt/progress tables; Phase 4 reuses them without a
migration. Registry/task details are in [SQL_GRADING.md](SQL_GRADING.md).

## Local use

```sh
docker compose up -d --build --wait
```

Open [lesson 10.2](http://localhost:3000/?lesson=s10-select-aliases-and-expressions).
The same workspace works in [10.3 WHERE](http://localhost:3000/?lesson=s10-where-and-boolean-logic)
and [10.4 NULL](http://localhost:3000/?lesson=s10-null-and-three-valued-logic).
Continue to [10.5 ORDER BY/LIMIT/OFFSET](http://localhost:3000/?lesson=s10-order-by-limit-and-offset)
and [10.6 DISTINCT](http://localhost:3000/?lesson=s10-distinct).
SQL Lab opens a `shop-v1` session automatically. Edit `query.sql`, press Run or
Ctrl/Cmd+Enter, inspect real PostgreSQL results. The Database tab shows table
columns, nullable/type metadata, ordered PK and FK pairs, and pages of 50 rows.
FK links select the referenced table, including users' self-reference.

Check (Ctrl/Cmd+Shift+Enter) evaluates four fixture revisions for
`sql.guided.10.2.projection.v1`, five for `sql.basic.01` (WHERE) and five for
`sql.basic.03` (NULL), and six each for `sql.basic.04` (latest orders) and
`sql.basic.05` (distinct countries). The last two use ordered comparison. It shows Passed/Failed, counts and task-aware safe
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
is wider than 420px. At viewport widths up to 820px, tabs preserve editing space.
Learn/Review and theme changes do not create another session or clear the draft.
The task answer is behind an explicit disclosure in the lesson, closed in both
modes. Guided-only capabilities do not render Check.

## Data ownership and persistence

`backend/app/sql_content.py` owns the capability mapping by stable lesson ID.
Its public manifest projects task ID/revision, prompt, starter, expected column
names, Check capability and persisted completion. It never returns reference SQL,
hidden fixtures, expected rows or grader rules.
Only these five published lessons get `workspace_kind=sql` in the lesson API.
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

For a manual browser check with the disposable DB:

```sh
docker compose build sandbox sql-sandbox sql-runner
docker compose -f docker-compose.sql-workspace-test.yml up -d --build --wait
# http://localhost:13000/?lesson=s10-select-aliases-and-expressions
python3 scripts/smoke_sql_workspace.py
docker compose -f docker-compose.sql-workspace-test.yml down
```

The real PostgreSQL execution/security tests from Phase 1 remain separate:
`scripts/test_sql_runner.sh`. Frontend tests exercise draft persistence, reset,
session cleanup and late responses, StrictMode, shortcuts, typed result/error
rendering, and navigation across Python/SQL without changing saved Python files.

See [SQL_GRADING.md](SQL_GRADING.md) for Phase 3 verification and upgrade evidence.
Browser interaction is covered by component tests; the real Docker HTTP smoke
exercises backend/runner/PostgreSQL, rather than a browser automation walkthrough.

Implementation references: [Monaco React](https://github.com/suren-atoyan/monaco-react),
[React effect cleanup](https://react.dev/reference/react/useEffect),
[FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/).
