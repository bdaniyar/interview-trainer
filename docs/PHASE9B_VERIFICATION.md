# Stage 11 PostgreSQL curriculum

| Lesson | Work in this PR | Executable evidence |
| --- | --- | --- |
| 11.1 Primary and Foreign Keys | Rewritten | Composite references, accepted rows and rejection with 23503 |
| 11.2 Constraints | Reviewed Phase 8B note | Exclusion constraint and concurrent conflict |
| 11.3 Normalization | Rewritten | Two order lines reconstruct independently stored associations |
| 11.4 Index Mental Model | Rewritten | Plans with and without an index, independently checked rows |
| 11.5 PostgreSQL B-tree | Rewritten | Ordered range query and a real optimizer plan |
| 11.6 Composite Indexes | Reviewed Phase 8B note | Existing PostgreSQL example and plan scenario |
| 11.7 Selectivity | Rewritten | Actual plans and buffers for a skewed fixture |
| 11.8 EXPLAIN and EXPLAIN ANALYZE | Reviewed Phase 8B note | Existing PostgreSQL example and plan scenario |
| 11.9 Transactions and ACID | Reviewed Phase 8B note | Real savepoint and rollback |
| 11.10 Isolation Levels | Reviewed Phase 8B note | Read Committed, Repeatable Read and Serializable |
| 11.11 MVCC | Reviewed Phase 8B note | Concurrent snapshots in A and B |
| 11.12 Locks | Reviewed Phase 8B note | PostgreSQL wait evidence, NOWAIT and SKIP LOCKED |
| 11.13 Deadlocks | Reviewed Phase 8B note | Real 40P01 victim and recovery |
| 11.14 Connection Pooling | Rewritten | FastAPI requests through AsyncEngine with one connection |
| 11.15 Pagination | Rewritten | Second page on tied timestamps, including an intervening insertion |
| 11.16 JSONB | Published | Typed containment and array queries, GIN setup and partial update |
| 11.17 Booking Concurrency | Reviewed Phase 8B note | Two-connection booking Check |

The eight reviewed notes include exercises, interview questions, disclosed
answers, expected results and primary sources. The previous nine curated notes
retain their IDs and examples. Review covered terminology, lesson ordering,
dependencies, schema assumptions, runnable blocks and closed answer disclosures.
JSONB builds on keys and the index mental model.

The content gate reports 406 taxonomy records, 370 published lessons, 68
Python task records and 222 legacy lessons across the full course. All 17
Stage 11 lessons are published and have curated provenance.

## Reproducible checks

- `scripts/test_stage11_examples.sh` executes seven checked-in SQL blocks and
  verifies 16 result sets. It runs the actual FastAPI lesson factory against
  PostgreSQL and checks three requests with a one-connection SQLAlchemy pool.
- `scripts/test_transaction_lab.sh` covers the existing notes and PostgreSQL
  scenarios through the workspace profile.
- `scripts/smoke_sql_browser.mjs` covers the previous workspace and checks
  closed JSONB answers and criteria in Learn and Review at desktop and mobile
  sizes. The focused entry point is `--stage11-only`.

The examples use PostgreSQL 17.11 and psycopg from the pinned lab image.
The FastAPI lesson uses FastAPI 0.116.1 and SQLAlchemy 2.0.43. Links in the
notes include the reference sections for PostgreSQL 17, SQLAlchemy 2.x,
FastAPI and PgBouncer. Review date is 18 November 2026. Example checks use
disposable synthetic data and do not mount the application data volume.
