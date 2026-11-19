# Phase 8D verification

The architecture review boundary builds on Phase 8C PR #13,
`fbb63ec3d84b41b41c1f7d7a602dea48e985dbe2`. While it remains unmerged this is a
stacked branch; dependencies are explicit and PRs are not merged automatically.

## Learning and project scope

Sixteen curated Russian notes cover 27.1–27.8, 27.12 and
29.1, 29.2, 29.4, 29.6, 29.7, 29.10, 29.11. The three prepared publications are
Microservices, Repository and Adapter. IDs, slugs, order, XP and interview positions
are preserved. Adapter now explicitly depends on published DI/Repository rather
than the still-planned Factory topic. Validated totals: 369 published / 406 taxonomy /
68 Python tasks, with 229 older lessons still editorial debt.

`projects/architecture_lab` implements the same workflow as a modular monolith and
two bounded HTTP services. Booking owns inventory/bookings/outbox; notification owns
inbox/effects. Separate application roles cannot CONNECT to the other service's DB.
The three synthetic DBs share one PostgreSQL cluster, hence one failure domain.
The monolith uses a common connection/transaction; distributed delivery uses stable
event IDs, hashes, durable inbox, unique business keys and a bounded leased relay.

The project has structured correlation logs, actual HTTP contracts and separate
entrypoints. Notes compare latency paths, consistency, releases, reliability, test
complexity and operational cost without invented measurements. They teach discovery,
tracing and saga fundamentals with explicit limits of this implementation.

## Verification status

| Check | Actual result |
| --- | --- |
| Default repository pytest | 288 passed, one existing upstream warning |
| Content validation | Passed: 369 / 406 / 68, editorial debt 229 |
| Frontend tests | 83 passed |
| Frontend lint / TypeScript / production build | Passed |
| Supported architecture project integrations | 16 passed with real PostgreSQL, HTTP and independent processes |
| Dev deployment and persistent restart probe | Passed with fresh owned volume/networks/loopback ports |
| Existing SELECT Docker integration suite | 216 passed in one complete invocation (30m53s) |
| Complete supported SQL Workspace HTTP script | Passed: all 23 SQL tasks, deliberate SQL outage and five Python assignments |
| Complete headless Chrome scenario | Passed: SQL/Python flow plus three architecture notes in Learn/Review |

The initial generator-preservation check caught `enrich_curriculum.py` restoring
Adapter's old Factory dependency in the taxonomy. The generator now takes explicit
dependencies from curated metadata, preserving the authored graph. The unchanged
full two-pass preservation regression then passed as part of the complete 288 run;
its digest comparison was not relaxed.

The supported `scripts/test_architecture_lab.sh` passed all 16 integrations: concurrent
last-unit booking, stable replay/conflict, monolith atomic rollback, distributed
intent rollback, unavailable receiver, HTTP timeout after receiver COMMIT, duplicate
event and conflicting payload, real producer process death after COMMIT, consumer
process restart, stale read before delivery, bounded retry/fencing, forbidden
cross-service CONNECT, strict HTTP inputs and two independent API processes.

`check_deployment.py` independently passed with fresh dev storage: the monolith
notification is immediate, distributed notification is initially absent and then
delivered, notification's container is recreated while booking's container remains
unchanged, event replay is idempotent, and a full PostgreSQL/container restart keeps
bookings, stock and inbox. Cleanup removes only that probe's fresh resources.

The complete SELECT suite also passed without failures, including pinned datasets,
typed reference/oracle results, adversarial grading, role/isolation/resource limits,
actual connection/controller failures and cleanup. The complete HTTP script then
passed correct/hardcoded/replay/sticky SQL progress, Explorer isolation, safe errors,
real Python Run/Check while SQL was deliberately offline, and all five Stage 20
assignments: 62 reference cases, 0 starter passes, replay XP=0, failed-retry stickiness,
two companion files and relative +100 XP only in the disposable test database.
The complete headless Chrome scenario passed native Monaco input and Run/Check for
all 23 SQL tasks and five Python tasks, preserved drafts/companion files, SQL/Python
round trips, theme/shortcuts, desktop 1720px and mobile 390px. It also navigated the
three new architecture publications and verified closed answers/criteria in both
Learn and Review. Microservices desktop/mobile captures were inspected after layout
settled; there is no page overflow. Architecture-note navigation did not award XP.

The host entered idle sleep during the long verification. Tests continued without
failure; a transient idle-sleep assertion was attached to the remaining pipeline
and released automatically on successful completion. Permanent power settings were
not changed.

## Main deployment and data preservation

`docker compose -p pythoria up -d --build --wait` completed. Frontend, backend and
Python Runner are healthy; the main catalog reports 369 published lessons. All 23
SQL manifests are available and every registered pinned bundle validates inside the
SQL controller. The two sandbox build helpers exited normally.

Consistent before/after snapshots mount `pythoria_pythoria_data` read-only. Both
schema/row hashes are
`ed4aab410c06523f9f78ae212705a8863b58e80adad91b768a939c4bc1cc8e08`.
No production Run/Check, data restoration or destructive migration was performed.
Python files, XP, previous lesson state and SQL progress remain intact.

## Limits

This is a local synthetic teaching environment with no authentication, real email or
payment provider. It does not implement a production saga orchestrator, cluster
failover, cross-version schema migrations, an operator retry UI or an OTel collector.
Correlation logs are implemented; a full trace/span deployment is an extension.
Separate ownership/deployment does not remove the shared PostgreSQL failure domain.
A transaction in booking cannot roll back an already committed notification.
Outbox preserves intent; arbitrary external exactly-once effects are not promised.

Existing SELECT/writable profiles, the four-second networkless Python Runner,
SQLite models and the AI curriculum plan stay unchanged. New project checks use
their own synthetic databases, tmpfs or freshly owned volumes; they never mount the
main Pythoria data volume. Main rebuild validation uses read-only source snapshots.
