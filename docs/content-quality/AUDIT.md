# Аудит опубликованных материалов Stage 8+

Автоматически проверены все перечисленные уроки. Это статический аудит известных дефектов, а не гарантия смысловой корректности. Содержательный аудит отмечен отдельно только у reviewed-комплектов.

| Этап | Опубликовано | Проверено содержательно | С детерминированными замечаниями |
| --- | ---: | ---: | ---: |
| 8 | 12 | 12 | 0 |
| 9 | 3 | 3 | 0 |
| 10 | 23 | 0 | 23 |
| 11 | 16 | 0 | 16 |
| 12 | 21 | 0 | 21 |
| 13 | 17 | 0 | 17 |
| 14 | 23 | 0 | 23 |
| 15 | 11 | 0 | 11 |
| 16 | 19 | 0 | 19 |
| 17 | 6 | 0 | 6 |
| 18 | 14 | 0 | 14 |
| 19 | 9 | 1 | 8 |
| 20 | 7 | 0 | 7 |
| 21 | 15 | 0 | 15 |
| 22 | 12 | 0 | 12 |
| 23 | 8 | 0 | 8 |
| 24 | 4 | 0 | 4 |
| 25 | 3 | 0 | 3 |
| 26 | 12 | 0 | 12 |
| 27 | 6 | 0 | 6 |
| 28 | 8 | 0 | 8 |
| 29 | 11 | 0 | 11 |
| 31 | 12 | 0 | 12 |
| 32 | 23 | 0 | 23 |

## Приоритеты

1. P0: архитектура сохранения bundles, порядок предпосылок Stage 8 и противоречивые interview rubric — исправлены; защита проверяется повторным запуском в копии репозитория.
2. P0: 12 подтверждённых подмен тем точечно исправлены: SQL, refresh sessions, pytest scope, Redis lists, Git index и listening port. Правила topic-mismatch защищают от возврата известных ошибочных абзацев. Полный аудит этих уроков остаётся в очереди.
3. P1: Stage 10–18 — следующий последовательный блок: SQL, PostgreSQL, HTTP, security, FastAPI, Pydantic, ORM, Alembic и testing. Требуется ручная переработка каждого legacy-урока, его задания и рубрики.
4. P1: закончить Stage 19 после отдельно исправленного 19.1; затем Stage 20–32 по порядку. Planned-уроки не публиковались.

## Покрытие по урокам

В audit.json сохранены коды и детали каждого замечания. «Ожидает аудита» означает, что содержательная корректность не подтверждена, даже если статические проверки не нашли ошибки.

- `backend-interview.8.3.await-and-cooperative-scheduling` (async-await): содержательно переработан; статических замечаний нет.
- `backend-interview.8.10.async-context-managers` (async-context-managers): содержательно переработан; статических замечаний нет.
- `backend-interview.8.11.async-iterators-and-generators` (async-iterators): содержательно переработан; статических замечаний нет.
- `backend-interview.8.8.cancellation` (cancellation): содержательно переработан; статических замечаний нет.
- `backend-interview.8.2.coroutine-function-and-coroutine-object` (coroutine): содержательно переработан; статических замечаний нет.
- `backend-interview.8.4.event-loop` (event-loop): содержательно переработан; статических замечаний нет.
- `backend-interview.8.6.asyncio-gather` (gather): содержательно переработан; статических замечаний нет.
- `backend-interview.9.2.multiprocessing` (processes): содержательно переработан; статических замечаний нет.
- `backend-interview.8.5.tasks-and-asyncio-create-task` (tasks): содержательно переработан; статических замечаний нет.
- `backend-interview.9.3.threadpoolexecutor` (thread-pool): содержательно переработан; статических замечаний нет.
- `backend-interview.9.1.threading` (threads): содержательно переработан; статических замечаний нет.
- `backend-interview.27.6.layered-architecture` (architecture-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.11.async-tests` (async-testing): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.1.basic-request-path` (backend-core-project): ожидает содержательного аудита; generic-copy.
- `backend-interview.27.7.dependency-injection` (dependency-injection): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.3.fixtures` (fixtures): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.6.mocking` (mocks): ожидает содержательного аудита; generic-copy.
- `backend-interview.27.5.separation-of-concerns` (package-design): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.5.parametrization` (parametrization): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.2.pytest-fundamentals` (pytest): ожидает содержательного аудита; generic-copy.
- `backend-interview.8.9.blocking-code-inside-async-code` (s08-blocking-code-inside-async-code): содержательно переработан; статических замечаний нет.
- `backend-interview.8.1.sync-concurrency-and-parallelism` (s08-sync-concurrency-and-parallelism): содержательно переработан; статических замечаний нет.
- `backend-interview.8.12.threads-vs-processes-vs-async` (s08-threads-vs-processes-vs-async): содержательно переработан; статических замечаний нет.
- `backend-interview.8.7.timeouts` (s08-timeouts): содержательно переработан; статических замечаний нет.
- `backend-interview.10.7.aggregates` (s10-aggregates): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.19.case` (s10-case): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.15.correlated-subquery` (s10-correlated-subquery): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.17.cte` (s10-cte): ожидает содержательного аудита; generic-copy, practice-unspecified.
- `backend-interview.10.25.data-modification` (s10-data-modification): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.6.distinct` (s10-distinct): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.16.exists-vs-in` (s10-exists-vs-in): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.8.group-by` (s10-group-by): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.9.having` (s10-having): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.10.inner-join` (s10-inner-join): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.11.left-join` (s10-left-join): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.4.null-and-three-valued-logic` (s10-null-and-three-valued-logic): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.5.order-by-limit-and-offset` (s10-order-by-limit-and-offset): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.23.partition-by-and-window-ordering` (s10-partition-by-and-window-ordering): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.1.relational-model-and-tables` (s10-relational-model-and-tables): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.12.right-and-full-outer-join` (s10-right-and-full-outer-join): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.22.row-number-rank-dense-rank` (s10-row-number-rank-dense-rank): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.2.select-aliases-and-expressions` (s10-select-aliases-and-expressions): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.13.self-join` (s10-self-join): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.20.set-operations` (s10-set-operations): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.14.subqueries` (s10-subqueries): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.3.where-and-boolean-logic` (s10-where-and-boolean-logic): ожидает содержательного аудита; generic-copy.
- `backend-interview.10.21.window-functions` (s10-window-functions): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.17.booking-concurrency` (s11-booking-concurrency): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.6.composite-indexes-and-column-order` (s11-composite-indexes-and-column-order): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.14.connection-pooling` (s11-connection-pooling): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.2.constraints` (s11-constraints): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.13.deadlocks` (s11-deadlocks): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.8.explain-and-explain-analyze` (s11-explain-and-explain-analyze): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.4.index-mental-model` (s11-index-mental-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.10.isolation-levels` (s11-isolation-levels): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.12.locks` (s11-locks): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.11.mvcc-basics` (s11-mvcc-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.3.normalization` (s11-normalization): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.15.pagination` (s11-pagination): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.5.postgresql-b-tree` (s11-postgresql-b-tree): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.1.primary-and-foreign-keys` (s11-primary-and-foreign-keys): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.7.selectivity` (s11-selectivity): ожидает содержательного аудита; generic-copy.
- `backend-interview.11.9.transactions-and-acid` (s11-transactions-and-acid): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.9.400-vs-422` (s12-400-vs-422): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.8.401-vs-403` (s12-401-vs-403): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.19.api-pagination-filtering-sorting` (s12-api-pagination-filtering-sorting): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.21.api-versioning-and-compatibility` (s12-api-versioning-and-compatibility): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.10.content-negotiation-and-content-type` (s12-content-negotiation-and-content-type): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.11.cookies` (s12-cookies): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.15.dns` (s12-dns): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.20.error-contracts` (s12-error-contracts): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.12.http-caching` (s12-http-caching): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.13.http-https-and-tls-basics` (s12-http-https-and-tls-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.3.http-methods` (s12-http-methods): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.1.http-request-and-response` (s12-http-request-and-response): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.14.ip-ports-and-sockets` (s12-ip-ports-and-sockets): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.22.openapi` (s12-openapi): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.2.path-query-headers-and-body` (s12-path-query-headers-and-body): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.6.post-vs-put` (s12-post-vs-put): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.5.put-vs-patch` (s12-put-vs-patch): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.18.rest-resources-and-urls` (s12-rest-resources-and-urls): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.17.reverse-proxy` (s12-reverse-proxy): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.4.safe-and-idempotent-methods` (s12-safe-and-idempotent-methods): ожидает содержательного аудита; generic-copy.
- `backend-interview.12.7.status-codes` (s12-status-codes): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.5.access-and-refresh-tokens` (s13-access-and-refresh-tokens): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.1.authentication-vs-authorization` (s13-authentication-vs-authorization): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.9.authorization-code-plus-pkce` (s13-authorization-code-plus-pkce): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.13.cors` (s13-cors): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.12.csrf` (s13-csrf): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.16.https-and-secure-cookies` (s13-https-and-secure-cookies): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.17.input-validation-and-file-upload-security` (s13-input-validation-and-file-upload-security): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.6.jwt-pitfalls` (s13-jwt-pitfalls): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.4.jwt-structure` (s13-jwt-structure): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.8.oauth2-basics` (s13-oauth2-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.2.password-storage` (s13-password-storage): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.15.rate-limiting` (s13-rate-limiting): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.13.7.rbac-and-permissions` (s13-rbac-and-permissions): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.14.secret-management` (s13-secret-management): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.3.sessions` (s13-sessions): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.10.sql-injection` (s13-sql-injection): ожидает содержательного аудита; generic-copy.
- `backend-interview.13.11.xss` (s13-xss): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.9.annotated-dependencies` (s14-annotated-dependencies): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.1.application-and-asgi-mental-model` (s14-application-and-asgi-mental-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.16.backgroundtasks` (s14-backgroundtasks): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.17.cors-configuration` (s14-cors-configuration): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.8.dependency-injection-with-depends` (s14-dependency-injection-with-depends): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.12.exception-handlers` (s14-exception-handlers): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.14.lifespan` (s14-lifespan): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.13.middleware` (s14-middleware): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.18.openapi-and-swagger` (s14-openapi-and-swagger): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.3.path-parameters` (s14-path-parameters): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.20.project-structure` (s14-project-structure): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.4.query-parameters` (s14-query-parameters): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.5.request-bodies` (s14-request-bodies): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.6.response-models` (s14-response-models): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.2.routes-and-routers` (s14-routes-and-routers): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.14.22.service-layer` (s14-service-layer): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.21.settings-configuration` (s14-settings-configuration): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.7.status-codes-headers-and-cookies` (s14-status-codes-headers-and-cookies): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.15.sync-vs-async-endpoints` (s14-sync-vs-async-endpoints): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.24.testing-fastapi` (s14-testing-fastapi): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.11.validation-errors` (s14-validation-errors): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.19.websockets` (s14-websockets): ожидает содержательного аудита; generic-copy.
- `backend-interview.14.10.yield-dependencies` (s14-yield-dependencies): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.1.basemodel-and-validation` (s15-basemodel-and-validation): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.10.configdict` (s15-configdict): ожидает содержательного аудита; generic-copy.
- `backend-interview.15.3.field-constraints` (s15-field-constraints): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.6.field-validators` (s15-field-validators): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.9.model-validate` (s15-model-validate): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.15.7.model-validators` (s15-model-validators): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.5.nested-models` (s15-nested-models): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.4.optional-nullable-and-default-values` (s15-optional-nullable-and-default-values): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.15.11.orm-integration` (s15-orm-integration): ожидает содержательного аудита; generic-copy.
- `backend-interview.15.2.parsing-vs-validation-mental-model` (s15-parsing-vs-validation-mental-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.15.8.serialization-and-model-dump` (s15-serialization-and-model-dump): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.8.add-flush-commit-and-refresh` (s16-add-flush-commit-and-refresh): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.17.async-engine-and-asyncsession` (s16-async-engine-and-asyncsession): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.18.async-lazy-loading-pitfalls` (s16-async-lazy-loading-pitfalls): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.16.cascade-and-delete-orphan` (s16-cascade-and-delete-orphan): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.19.constraints-and-indexes-in-models` (s16-constraints-and-indexes-in-models): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.2.declarative-models` (s16-declarative-models): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.1.engine-and-connection-pool` (s16-engine-and-connection-pool): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.10.explicit-transactions` (s16-explicit-transactions): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.15.joinedload` (s16-joinedload): ожидает содержательного аудита; duplicate-practice, generic-copy, task-contract.
- `backend-interview.16.11.joins` (s16-joins): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.12.lazy-loading` (s16-lazy-loading): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.13.n-plus-1` (s16-n-plus-1): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.3.relationships` (s16-relationships): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.9.rollback` (s16-rollback): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.14.selectinload` (s16-selectinload): ожидает содержательного аудита; duplicate-practice, generic-copy, task-contract.
- `backend-interview.16.7.session-get` (s16-session-get): ожидает содержательного аудита; duplicate-practice, generic-copy, task-contract.
- `backend-interview.16.5.session-lifecycle` (s16-session-lifecycle): ожидает содержательного аудита; generic-copy.
- `backend-interview.16.4.session-mental-model` (s16-session-mental-model): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.16.6.sqlalchemy-2-x-select` (s16-sqlalchemy-2-x-select): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.17.3.autogenerate` (s17-autogenerate): ожидает содержательного аудита; generic-copy, task-contract.
- `backend-interview.17.4.data-migrations` (s17-data-migrations): ожидает содержательного аудита; generic-copy.
- `backend-interview.17.6.migration-history-conflicts` (s17-migration-history-conflicts): ожидает содержательного аудита; generic-copy.
- `backend-interview.17.2.revision-upgrade-and-downgrade` (s17-revision-upgrade-and-downgrade): ожидает содержательного аудита; generic-copy.
- `backend-interview.17.5.safe-schema-changes` (s17-safe-schema-changes): ожидает содержательного аудита; generic-copy.
- `backend-interview.17.1.why-migrations-exist` (s17-why-migrations-exist): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.13.coverage` (s18-coverage): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.9.database-tests` (s18-database-tests): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.8.fastapi-tests` (s18-fastapi-tests): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.4.fixture-scope` (s18-fixture-scope): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.7.monkeypatch-mock-and-asyncmock` (s18-monkeypatch-mock-and-asyncmock): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.10.redis-tests` (s18-redis-tests): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.14.test-isolation-and-determinism` (s18-test-isolation-and-determinism): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.1.test-pyramid-and-test-types` (s18-test-pyramid-and-test-types): ожидает содержательного аудита; generic-copy.
- `backend-interview.18.12.what-to-test` (s18-what-to-test): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.7.atomic-counters-and-rate-limiting` (s19-atomic-counters-and-rate-limiting): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.4.cache-aside` (s19-cache-aside): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.5.cache-invalidation` (s19-cache-invalidation): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.2.data-structures` (s19-data-structures): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.10.redis-failure-scenarios` (s19-redis-failure-scenarios): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.1.redis-mental-model` (s19-redis-mental-model): содержательно переработан; статических замечаний нет.
- `backend-interview.19.8.redis-pub-sub` (s19-redis-pub-sub): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.6.sessions-and-temporary-state` (s19-sessions-and-temporary-state): ожидает содержательного аудита; generic-copy.
- `backend-interview.19.3.ttl-and-expiration` (s19-ttl-and-expiration): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.3.celery-model` (s20-celery-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.2.fastapi-backgroundtasks` (s20-fastapi-backgroundtasks): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.5.idempotency` (s20-idempotency): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.1.in-request-vs-background-work` (s20-in-request-vs-background-work): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.7.outbox-pattern` (s20-outbox-pattern): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.20.4.retry-and-backoff` (s20-retry-and-backoff): ожидает содержательного аудита; generic-copy.
- `backend-interview.20.8.why-outbox-instead-of-direct-celery-publish` (s20-why-outbox-instead-of-direct-celery-publish): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.12.build-vs-image` (s21-build-vs-image): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.4.build-vs-run` (s21-build-vs-run): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.15.compose-commands` (s21-compose-commands): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.14.compose-volumes-networks-env-file` (s21-compose-volumes-networks-env-file): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.16.container-debugging` (s21-container-debugging): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.13.depends-on-and-readiness` (s21-depends-on-and-readiness): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.11.docker-compose-services` (s21-docker-compose-services): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.2.dockerfile` (s21-dockerfile): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.9.dockerignore` (s21-dockerignore): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.7.environment-variables` (s21-environment-variables): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.21.1.image-vs-container` (s21-image-vs-container): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.3.layers-and-cache` (s21-layers-and-cache): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.8.networks-and-service-discovery` (s21-networks-and-service-discovery): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.5.port-mapping` (s21-port-mapping): ожидает содержательного аудита; generic-copy.
- `backend-interview.21.6.volumes` (s21-volumes): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.3.branch-and-switch` (s22-branch-and-switch): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.7.conflict-resolution` (s22-conflict-resolution): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.4.fetch-pull-and-push` (s22-fetch-pull-and-push): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.10.gitignore-and-secrets` (s22-gitignore-and-secrets): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.2.init-clone-status-add-and-commit` (s22-init-clone-status-add-and-commit): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.5.merge` (s22-merge): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.12.practical-git-scenarios` (s22-practical-git-scenarios): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.11.pull-request-and-code-review` (s22-pull-request-and-code-review): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.6.rebase-basics` (s22-rebase-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.1.repository-working-tree-index-and-commit` (s22-repository-working-tree-index-and-commit): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.9.reset-vs-revert` (s22-reset-vs-revert): ожидает содержательного аудита; generic-copy.
- `backend-interview.22.8.stash` (s22-stash): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.8.application-logs-and-exit-codes` (s23-application-logs-and-exit-codes): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.4.environment-variables` (s23-environment-variables): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.23.2.file-operations` (s23-file-operations): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.1.filesystem-navigation` (s23-filesystem-navigation): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.6.permissions` (s23-permissions): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.7.ports-and-network-diagnostics` (s23-ports-and-network-diagnostics): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.5.processes` (s23-processes): ожидает содержательного аудита; generic-copy.
- `backend-interview.23.3.reading-searching-logs-and-files` (s23-reading-searching-logs-and-files): ожидает содержательного аудита; generic-copy.
- `backend-interview.24.5.ci-debugging` (s24-ci-debugging): ожидает содержательного аудита; generic-copy.
- `backend-interview.24.1.ci-pipeline-mental-model` (s24-ci-pipeline-mental-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.24.3.github-actions-or-existing-ci` (s24-github-actions-or-existing-ci): ожидает содержательного аудита; generic-copy.
- `backend-interview.24.4.quality-gates` (s24-quality-gates): ожидает содержательного аудита; generic-copy.
- `backend-interview.25.7.backend-signals` (s25-backend-signals): ожидает содержательного аудита; generic-copy.
- `backend-interview.25.1.logging-fundamentals` (s25-logging-fundamentals): ожидает содержательного аудита; generic-copy.
- `backend-interview.25.3.logs-vs-metrics-vs-traces` (s25-logs-vs-metrics-vs-traces): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.8.apiview-generic-views-and-viewset` (s26-apiview-generic-views-and-viewset): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.9.authentication-and-permissions` (s26-authentication-and-permissions): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.4.django-orm-query-basics` (s26-django-orm-query-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.1.django-project-app-mental-model` (s26-django-project-app-mental-model): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.11.drf-exception-response-flow` (s26-drf-exception-response-flow): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.7.drf-serializers` (s26-drf-serializers): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.12.drf-testing` (s26-drf-testing): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.13.fastapi-vs-django-drf` (s26-fastapi-vs-django-drf): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.3.models-and-migrations` (s26-models-and-migrations): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.10.pagination-filtering` (s26-pagination-filtering): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.5.select-related-and-prefetch-related` (s26-select-related-and-prefetch-related): ожидает содержательного аудита; generic-copy.
- `backend-interview.26.2.settings-and-environment` (s26-settings-and-environment): ожидает содержательного аудита; generic-copy.
- `backend-interview.27.4.coupling-and-cohesion` (s27-coupling-and-cohesion): ожидает содержательного аудита; generic-copy.
- `backend-interview.27.2.modular-monolith` (s27-modular-monolith): ожидает содержательного аудита; generic-copy.
- `backend-interview.27.1.monolith` (s27-monolith): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.2.array-list` (s28-array-list): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.8.backend-oriented-coding-set` (s28-backend-oriented-coding-set): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.1.big-o` (s28-big-o): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.6.binary-search` (s28-binary-search): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.3.hash-table-dict-set` (s28-hash-table-dict-set): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.5.queue-deque` (s28-queue-deque): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.7.sorting-basics` (s28-sorting-basics): ожидает содержательного аудита; generic-copy.
- `backend-interview.28.4.stack` (s28-stack): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.4.background-jobs` (s29-background-jobs): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.6.booking-endpoint` (s29-booking-endpoint): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.3.cache-placement` (s29-cache-placement): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.8.chat-websocket-design` (s29-chat-websocket-design): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.5.database-bottlenecks` (s29-database-bottlenecks): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.9.file-upload-design` (s29-file-upload-design): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.10.outbox-design` (s29-outbox-design): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.7.preventing-double-booking` (s29-preventing-double-booking): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.11.scaling-sequence` (s29-scaling-sequence): ожидает содержательного аудита; generic-copy.
- `backend-interview.29.2.stateless-api-and-horizontal-scaling` (s29-stateless-api-and-horizontal-scaling): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.8.difficult-bug` (s31-difficult-bug): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.12.english-project-explanation` (s31-english-project-explanation): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.11.student-schedule-and-availability` (s31-student-schedule-and-availability): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.10.teamwork-and-code-review` (s31-teamwork-and-code-review): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.1.tell-me-about-yourself` (s31-tell-me-about-yourself): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.9.what-would-you-improve` (s31-what-would-you-improve): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.3.why-backend` (s31-why-backend): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.7.why-docker` (s31-why-docker): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.4.why-fastapi` (s31-why-fastapi): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.5.why-postgresql` (s31-why-postgresql): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.2.why-python` (s31-why-python): ожидает содержательного аудита; generic-copy.
- `backend-interview.31.6.why-redis` (s31-why-redis): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.15.alembic` (s32-alembic): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.19.celery-workers` (s32-celery-workers): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.23.honest-boundaries` (s32-honest-boundaries): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.17.hotel-booking-and-double-booking` (s32-hotel-booking-and-double-booking): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.11.jwt-refresh-sessions` (s32-jwt-refresh-sessions): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.14.minio-and-presigned-urls` (s32-minio-and-presigned-urls): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.10.multiple-outbox-workers` (s32-multiple-outbox-workers): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.21.oauth2-authorization-code-plus-pkce` (s32-oauth2-authorization-code-plus-pkce): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.8.outbox-pattern` (s32-outbox-pattern): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.32.20.prometheus-grafana-sentry` (s32-prometheus-grafana-sentry): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.16.pytest-and-80-coverage-gate` (s32-pytest-and-80-coverage-gate): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.13.rate-limiting` (s32-rate-limiting): ожидает содержательного аудита; duplicate-practice, generic-copy.
- `backend-interview.32.22.redis-backed-password-reset` (s32-redis-backed-password-reset): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.18.redis-caching-in-hotel-booking` (s32-redis-caching-in-hotel-booking): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.12.roles-and-permissions` (s32-roles-and-permissions): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.1.studyhub-in-60-seconds` (s32-studyhub-in-60-seconds): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.6.websockets-plus-redis-pub-sub` (s32-websockets-plus-redis-pub-sub): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.4.why-async` (s32-why-async): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.3.why-one-backend-language` (s32-why-one-backend-language): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.9.why-outbox-instead-of-celery-in-studyhub` (s32-why-outbox-instead-of-celery-in-studyhub): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.5.why-postgresql-and-redis-together` (s32-why-postgresql-and-redis-together): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.7.why-pub-sub-is-not-storage` (s32-why-pub-sub-is-not-storage): ожидает содержательного аудита; generic-copy.
- `backend-interview.32.2.why-python-and-fastapi` (s32-why-python-and-fastapi): ожидает содержательного аудита; generic-copy.
