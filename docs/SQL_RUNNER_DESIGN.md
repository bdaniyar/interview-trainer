# SQL runner status and safe extension plan

The repository currently has one execution mode: isolated Python/pytest. SQL practice is published as PostgreSQL-compatible schema, seed, prompt, expected columns, comparison mode and hidden solution/rubric, but the UI does not claim that SQL is executable.

Adding SQL to the Python container would weaken isolation and teach SQLite behavior where PostgreSQL semantics matter. A future implementation should use a separate disposable PostgreSQL service or per-attempt schema with:

- a non-owner role without filesystem, network or administration privileges;
- one parsed statement by default and an explicit allowlist for lesson DDL;
- statement timeout, transaction timeout and row/output limits;
- fresh schema and seed for every run;
- rollback/drop after every attempt;
- ordered or unordered result comparison from task metadata;
- hidden datasets supplied only by the backend;
- no production credentials and no access to application SQLite.

The structured backlog is content/practice_banks.json. Its SQL records are ready for a future execution adapter without changing lesson IDs or progress keys.
