# SQL Workspace — Phase 2

Enabled for **10.2**, stable lesson ID
`backend-interview.10.2.select-aliases-and-expressions`, slug
`s10-select-aliases-and-expressions`. The rest of the course keeps its existing
workspace. No lesson IDs, task completion, XP rules or database tables change.

## Local use

```sh
docker compose up -d --build --wait
```

Open [lesson 10.2](http://localhost:3000/?lesson=s10-select-aliases-and-expressions).
SQL Lab opens a `shop-v1` session automatically. Edit `query.sql`, press Run or
Ctrl/Cmd+Enter, inspect real PostgreSQL results. The Database tab shows table
columns, nullable/type metadata, ordered PK and FK pairs, and pages of 50 rows.
FK links select the referenced table, including users' self-reference.

Refresh updates catalog/data. Reset creates a fresh baseline and rotates the
generation/handles, preserving the editor text. Result diagnostics include
SQLSTATE and a clickable editor position; Unicode positions are translated to
Monaco's UTF-16 columns. Query errors/cells are rendered as text. Duplicate
aliases, NULL, empty string, booleans, bigint/numeric and empty results remain
distinct. Truncated results say there are more rows, without inventing a total.

On narrow workspaces, tabs keep Editor, Database and Results usable. Learn/Review
and theme changes do not create another session or clear the SQL draft. SQL Lab
has no Python terminal, solution button, Check or SQL rewards.

## Data ownership and persistence

`backend/app/sql_content.py` owns the capability mapping by stable lesson ID.
Its public manifest describes a guided SELECT activity; it never loads or returns
practice-bank solutions, expected reasoning, hidden fixtures or grading fields.
Only this published lesson gets `workspace_kind=sql` in the existing lesson API.

SQL drafts are stored **only in this browser** under
`pythoria:sql:<stable-lesson-id>:guided-select`. Each edit is saved synchronously;
Ctrl/Cmd+S also saves locally. Storage errors are displayed without clearing the
editor. SQL never goes to the Python `/files` endpoint. CourseApp saves Python
files against the loaded Python lesson before navigation, and unmounts its Python
workspace/listeners when SQL is active.

The backend holds at most two ephemeral bindings, from a new public opaque ID to
the runner's private session ID, fixed local principal, lesson and generation.
It validates binding/generation before forwarding and rewrites IDs in responses.
Clients cannot choose owner, dataset, image, paths, credentials or budgets. Per
binding admission fails fast on concurrent Run/Reset; the runner still enforces
its global limits independently. No SQL route opens an SQLite transaction or
executes a database driver. Requests use a separate bounded HTTP client, with
35-second provisioning/reset and 15-second other request timeouts. The SQL request
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
durable playground databases, immediate query cancellation, grading and XP belong
to later phases.

## Public backend API

| Endpoint | Contract |
| --- | --- |
| `GET /api/sql/lessons/{slug}` | Guided public manifest; unsupported/unpublished lesson returns 404 |
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

Local verification on 2026-11-11: **173 Python tests, 19 frontend tests**, content
validation, lint, TypeScript and production builds passed. Both the Docker HTTP
smoke and the SQL-controller-outage/Python regression smoke passed. The disposable
stack was removed and no SQL sandboxes remained. User persistence was never
mounted in this environment.

Native Chrome rendered the real Monaco SQL editor and an active session. Window
control errors prevented completing the remaining manual clicks; interactive
scenarios are covered by component tests and the real backend/runner HTTP smoke.

Implementation references: [Monaco React](https://github.com/suren-atoyan/monaco-react),
[React effect cleanup](https://react.dev/reference/react/useEffect),
[FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/).
