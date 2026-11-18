# Phase 9A verification

The baseline is `37d184f2bc06ef4b448e33f5f9a25148f6ea466c` on
`feat/durable-workers-phase8c`. PR #13 reached main at
`082aff9081313a2af0a847481901abc8228b1736`. PR #14 was merged into its
original feature base, where its architecture lessons and project are present.
The Phase 9A review targets that branch and contains only the Transaction Lab work.

## Transaction Lab

The existing writable profile serves two real PostgreSQL connections in a
disposable container. The resident process owns A and B, and a third observer
checks `pg_blocking_pids` and reads committed synthetic rows. Each learner
connection admits one command at a time. Run returns an operation ID while
the work continues. A busy connection does not prevent COMMIT or ROLLBACK on
the other. PostgreSQL supplies SQLSTATE, transaction state and typed rows.
Reset removes the old container and increments the generation. URLs bind
the random session and operation IDs to the lesson and generation.

The CLI coordinator's original grader supplies six independent datasets per
task. Its policy, fixtures, task IDs and revision remain the same. Web Check
records outcomes in the existing SQL attempts and progress tables keyed by
the two distinct transaction IDs. Replay detects a changed request body,
and a later failure does not erase a completed task. Schema extension and
XP changes are unnecessary.

The workstation Compose service is private. The networkless sandbox uses the
existing student UID and PostgreSQL role. No user path, image, mount, command,
DSN or internal handle is accepted by the public API. The root filesystem is
read-only, Docker resources keep their existing bounds, and the watchdog
removes abandoned sessions. A/B drafts live in separate browser keys.

## Verification

- 289 default pytest tests passed. 83 frontend tests, ESLint, TypeScript,
  build and content validation passed.
- The complete Transaction Lab Docker suite passed 52 tests, including
  the previous 44 and eight web coordinator cases. Tests exercise an
  actual blocked query, COMMIT and ROLLBACK release, NOWAIT, SQL cancellation,
  independent session state, generation reset, expiry, container crash,
  a paused container deadline and startup reaping.
- The PostgreSQL idle transaction deadline rolls back the holder, marks that
  connection disconnected and allows the next Run to reconnect.
- The disposable HTTP test passed both Check contracts at 6/6 and proved
  replay, changed-body conflict, preserved completion after failed Check,
  preserved existing files and XP, completion after Reset, and replay
  after backend restart.
  It also closes the client socket after submitting a waiting Run. The
  server observes the operation and releases it using the other connection.
- A focused Chrome run passed native A/B Monaco input, blocking and release,
  Serializable 40001, valid and invalid checks, Learn/Review, draft and
  completion restoration, theme, desktop/mobile and SQL/Python navigation.
  Desktop and 390 px captures were inspected.
- The first full SELECT regression recorded 214 passes out of 216. The
  JOIN catalog and crash-cleanup checks passed a targeted repeat. The
  complete post-fix run is in progress.
- The first combined HTTP regression stopped at the old projection task's
  invalid-cast assertion. The complete Chrome walkthrough reached seven
  SELECT tasks before the runner became unavailable. These shared
  regressions need a serial repeat.
- The primary Compose project rebuilt and verified both transaction
  manifests and all 23 pinned SELECT bundles. The SQLite logical digest
  matched before and after.

Verification found and corrected a Docker auto-remove race in the shared
Docker coordinator, a product race
between polling and Run, and a mismatch between a scenario result shape and
its renderer. One HTTP attempt returned runner unavailable during Booking
Check. The passing repeat did not require higher deadlines. Operational
logging records the trusted stage and exception type for later diagnosis.
The legacy timeout exception remains distinct.

The 60-second container lifetime, 5-second idle transaction limit and
1.5-second lock wait limit carry over from the CLI. Use prepared commands
for live races or run one of the twelve deterministic demonstrations.
