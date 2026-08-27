# Content and runtime inventory

Audit date: 2026-08-27.

## Current architecture

- Frontend: React 19, TypeScript 5.9, Vinext/Vite 8, Monaco Editor and xterm.js.
- Backend: FastAPI 0.116, Pydantic 2.11, SQLAlchemy 2.0 and SQLite.
- Runner: isolated Python 3.12 Docker container with network disabled, resource limits, four-second timeout and clipped output.
- Content source: `content/<module>/<lesson>/metadata.json` plus Markdown, starter files, hidden tests, solutions and interview JSON.
- Stable progress key: lesson `slug`; existing slugs must never be renamed or reused for another topic.
- Navigation is discovered from lesson metadata and sorted by the global `order` field.

## Content capabilities

| Capability | Existing implementation | Authoring location |
| --- | --- | --- |
| Theory | GFM Markdown | `lesson.md` |
| Python task | Monaco workspace | `starter/` |
| Hidden check | pytest in sandbox | `tests/` |
| Reference solution | Backend-only endpoint | `solution/` |
| Interview question | Structured local JSON | `interview.json` |
| Progress/XP | SQLite | backend models and API |
| SQL execution | Not implemented | static PostgreSQL-compatible tasks only |

Unknown metadata fields are already passed through without a destructive database migration. The curriculum therefore extends lesson metadata in a backward-compatible way and keeps `slug` as the persistence key.

## Baseline before curriculum population

- 67 discoverable lessons in five modules.
- Six lessons with working Python tasks and hidden tests.
- 61 placeholder lessons.
- Six interview JSON files.
- No SQL runner and no abstraction for multiple execution modes.
- No frontend unit-test command; frontend verification is lint plus production build.

## Commands

```bash
python3 -m pytest backend/tests runner/tests -q
cd frontend && npm run lint && npm run build
python3 tools/validate_content.py
docker compose up --build
python3 scripts/smoke_test.py
```

## Compatibility decisions

1. Existing lesson slugs and saved progress remain valid.
2. New taxonomy metadata is additive; database tables do not require a migration.
3. P2/P3 taxonomy records use `content_status: planned` until authored and are not published as empty pages.
4. PostgreSQL practice is fully specified but not executed until a disposable PostgreSQL runner can be added without weakening the Python sandbox.
5. Hidden tests and solutions remain backend-only and never enter the frontend bundle.
