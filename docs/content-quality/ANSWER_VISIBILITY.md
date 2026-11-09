# Скрытие ответов в Learn и Review

Дата: 2026-11-09. Основа: main после merge PR #1 (`a34c747`).

## Покрытие и счётчики

- Проверены все 295 опубликованных уроков Stage 8+ с учётом module_order, включая legacy-папки concurrency и reliability.
- В исходной версии найдено 206 открытых маркеров ответов/критериев в 94 уроках. Маркеры — диагностические совпадения, а не число независимых вопросов: один legacy-разбор содержал и критерии, и слабый ответ.
- Изменён Markdown 95 уроков: все 16 curated-уроков и 79 legacy-уроков. В 8.12 открытого маркера не было, но добавлена такая же закрытая самопроверка для трёх существующих вопросов.
- Добавлено 143 закрытых disclosure-блока: 49 ответов на практические вопросы curated-уроков, 92 существующих legacy-разбора и два разбора неавтоматических reasoning tasks (9.1 и 19.1).
- После изменений структурный сканер не находит известных утечек. Публичные разделы всех 63 coding tasks совпадают с исходной версией по SHA-256.

## Содержание и отображение

Вопросы отделены от ответов явно в lesson.md: `<details><summary>Показать ответ</summary>…</details>`. В Learn теория, учебные примеры и их разбор остаются открытыми; практика не содержит ответа в строке вопроса. В Review показываются вопросы, код для prediction и публичные условия coding tasks, а ответы и критерии раскрываются пользователем.

В 79 legacy-уроках только обёрнуты существующие пары «Критерии ответа / Слабый ответ»: сценарии, названия и формулировки не переписаны. Условия программных упражнений, включая input/output, ограничения и edge cases, не скрываются. Готовые реализации в тексты задач не добавлены. Содержательная переработка оставшихся 279 legacy-уроков не входила в эту задачу.

MarkdownLesson использует структурное разделение заголовков и disclosures с учётом fenced code. Заголовок внутри кода или скрытого ответа не превращается в отдельную открытую секцию. Поддерживаются переносы между details и summary, вложенные disclosures и Markdown/code blocks в ответах. Секция контента получает ключ lesson.slug + mode: переключение Learn/Review или урока создаёт закрытые disclosures заново, включая «Хорошие ответы» и «Критерии хорошего ответа».

Слова «Ответ» не используются для runtime-скрытия текста. Если закрывающий тег повреждён, renderer удерживает остаток ответа внутри disclosure; validator отклоняет такой контент.

## Защита и совместимость

Новый структурный проход validator проверяет только review-visible упражнения, исключая скрытые ответы и code fences. Он обнаруживает открытые Ответ / Ответ для самопроверки / Правильный ответ / Критерии ответа / Решение, открытый output-блок prediction, отдельный открытый заголовок «Решение»/«Исправленный код», совпадение Python-реализации в разделе задачи с solution/main.py, дубликат скрытого ответа в открытом тексте и неправильные disclosure (нет summary/закрытия, атрибут open, тег посреди строки). Ожидаемый вывод в условии программного упражнения разрешён. Эти ошибки блокируют обычную валидацию и в legacy-долге, а не только у curated-материалов.

IDs, slugs, metadata, interview.json, порядок интервью, XP, course.json, starter, solution, hidden tests, API и schema БД не менялись. Stage 1–7 побайтово сохранены. Snapshot не экспортировался, поскольку metadata не менялись. Предыдущая защита авторских генераторов сохранена и проходит regression checks.

## Код и тестовая инфраструктура

Изменены `frontend/app/components/MarkdownLesson.tsx`, `tools/content_quality.py`, `tools/validate_content.py`. Добавлены структурные readers `frontend/app/components/lessonMarkdown.ts` и `tools/lesson_markdown.py`, UI regression tests `frontend/tests/MarkdownLesson.test.tsx`, конфигурация `frontend/vitest.config.ts`, проверки `tools/tests/test_answer_visibility.py` и baseline публичных условий `tools/tests/fixtures/answer-leak-task-contracts.json`. В frontend/package.json и lockfile добавлена только тестовая инфраструктура Vitest + React Testing Library + jsdom и команда npm run test. Runtime-логика приложения не зависит от тестовых библиотек.

## Автоматические проверки

- `python3 tools/validate_content.py`: проходит (406 taxonomy, 359 published, 63 executable tasks; исторический содержательный долг 279 явно сохранён).
- `python3 -m pytest`: 36 passed, включая новую проверку, что утечка в legacy-уроке блокирует обычный validator; SHA-256 63 публичных coding contracts, предыдущие checks persistence keys, Stage 1–7 и повторного запуска генераторов.
- `npm run test`: 8 frontend-тестов проходят на настоящем Markdown 8.1, 8.9 и parametrization. Проверяются закрытие по умолчанию, раскрытие/закрытие, Learn → Review → Learn, смена урока, видимость coding contract и fenced code в ответах.
- Frontend lint, typecheck и build проходят. Сохранено существующее предупреждение build о размере chunks.

## Проверка в браузере

Проверка выполнена в Chrome на отдельном локальном preview новой ветки с временной SQLite БД. Пользовательская БД и Docker volumes не использовались для записи тестового прогресса.

- 8.1: в Learn вопрос без готового ответа; в Review ответ закрыт. Явное раскрытие показывает 7 и 4 с объяснением; повторное закрытие скрывает его. После перехода обратно в Learn ответ закрыт заново.
- 8.9: в Review виден вопрос про asyncio.to_thread(requests.get(url)), а объяснение ошибки закрыто; теория и исправленный пример из Learn не показываются.
- Parametrization: в Review видны программа и вопрос prediction, а 3 passed отсутствует до раскрытия. После клика результат и разбор появляются внутри ответа; code block отображается.
- Coding tasks: проверены публичные сигнатуры, input/output, пустой вход и ValueError в 8.1; сигнатура call_blocking и пример Aida! в 8.9. Сохранение, Check и начисление XP не требовались для этой проверки.

## Границы проверки

Детерминированные правила не доказывают отсутствие всех смысловых подсказок, сформулированных без маркеров. Известные найденные случаи исправлены; нерешённых структурных утечек сканер не показывает. Исторический содержательный долг не объявляется устранённым.

## Изменённые уроки

- `backend-interview.8.3.await-and-cooperative-scheduling` — `content/concurrency/async-await/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.10.async-context-managers` — `content/concurrency/async-context-managers/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.11.async-iterators-and-generators` — `content/concurrency/async-iterators/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.8.cancellation` — `content/concurrency/cancellation/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.2.coroutine-function-and-coroutine-object` — `content/concurrency/coroutine/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.4.event-loop` — `content/concurrency/event-loop/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.6.asyncio-gather` — `content/concurrency/gather/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.9.2.multiprocessing` — `content/concurrency/processes/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.5.tasks-and-asyncio-create-task` — `content/concurrency/tasks/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.9.3.threadpoolexecutor` — `content/concurrency/thread-pool/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.9.1.threading` — `content/concurrency/threads/lesson.md`; новых закрытых блоков: 4.
- `backend-interview.18.11.async-tests` — `content/reliability/async-testing/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.1.basic-request-path` — `content/reliability/backend-core-project/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.3.fixtures` — `content/reliability/fixtures/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.6.mocking` — `content/reliability/mocks/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.5.parametrization` — `content/reliability/parametrization/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.2.pytest-fundamentals` — `content/reliability/pytest/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.8.9.blocking-code-inside-async-code` — `content/stage-08/s08-blocking-code-inside-async-code/lesson.md`; новых закрытых блоков: 4.
- `backend-interview.8.1.sync-concurrency-and-parallelism` — `content/stage-08/s08-sync-concurrency-and-parallelism/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.12.threads-vs-processes-vs-async` — `content/stage-08/s08-threads-vs-processes-vs-async/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.8.7.timeouts` — `content/stage-08/s08-timeouts/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.10.8.group-by` — `content/stage-10/s10-group-by/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.10.10.inner-join` — `content/stage-10/s10-inner-join/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.10.11.left-join` — `content/stage-10/s10-left-join/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.10.5.order-by-limit-and-offset` — `content/stage-10/s10-order-by-limit-and-offset/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.11.13.deadlocks` — `content/stage-11/s11-deadlocks/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.11.8.explain-and-explain-analyze` — `content/stage-11/s11-explain-and-explain-analyze/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.11.4.index-mental-model` — `content/stage-11/s11-index-mental-model/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.11.9.transactions-and-acid` — `content/stage-11/s11-transactions-and-acid/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.13.5.access-and-refresh-tokens` — `content/stage-13/s13-access-and-refresh-tokens/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.13.13.cors` — `content/stage-13/s13-cors/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.13.6.jwt-pitfalls` — `content/stage-13/s13-jwt-pitfalls/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.13.2.password-storage` — `content/stage-13/s13-password-storage/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.13.10.sql-injection` — `content/stage-13/s13-sql-injection/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.14.lifespan` — `content/stage-14/s14-lifespan/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.6.response-models` — `content/stage-14/s14-response-models/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.22.service-layer` — `content/stage-14/s14-service-layer/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.7.status-codes-headers-and-cookies` — `content/stage-14/s14-status-codes-headers-and-cookies/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.15.sync-vs-async-endpoints` — `content/stage-14/s14-sync-vs-async-endpoints/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.14.24.testing-fastapi` — `content/stage-14/s14-testing-fastapi/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.8.add-flush-commit-and-refresh` — `content/stage-16/s16-add-flush-commit-and-refresh/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.17.async-engine-and-asyncsession` — `content/stage-16/s16-async-engine-and-asyncsession/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.18.async-lazy-loading-pitfalls` — `content/stage-16/s16-async-lazy-loading-pitfalls/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.16.cascade-and-delete-orphan` — `content/stage-16/s16-cascade-and-delete-orphan/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.12.lazy-loading` — `content/stage-16/s16-lazy-loading/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.16.13.n-plus-1` — `content/stage-16/s16-n-plus-1/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.16.9.rollback` — `content/stage-16/s16-rollback/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.9.database-tests` — `content/stage-18/s18-database-tests/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.8.fastapi-tests` — `content/stage-18/s18-fastapi-tests/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.4.fixture-scope` — `content/stage-18/s18-fixture-scope/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.7.monkeypatch-mock-and-asyncmock` — `content/stage-18/s18-monkeypatch-mock-and-asyncmock/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.10.redis-tests` — `content/stage-18/s18-redis-tests/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.14.test-isolation-and-determinism` — `content/stage-18/s18-test-isolation-and-determinism/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.18.1.test-pyramid-and-test-types` — `content/stage-18/s18-test-pyramid-and-test-types/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.19.7.atomic-counters-and-rate-limiting` — `content/stage-19/s19-atomic-counters-and-rate-limiting/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.19.5.cache-invalidation` — `content/stage-19/s19-cache-invalidation/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.19.2.data-structures` — `content/stage-19/s19-data-structures/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.19.1.redis-mental-model` — `content/stage-19/s19-redis-mental-model/lesson.md`; новых закрытых блоков: 4.
- `backend-interview.19.8.redis-pub-sub` — `content/stage-19/s19-redis-pub-sub/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.19.3.ttl-and-expiration` — `content/stage-19/s19-ttl-and-expiration/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.21.13.depends-on-and-readiness` — `content/stage-21/s21-depends-on-and-readiness/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.21.9.dockerignore` — `content/stage-21/s21-dockerignore/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.21.8.networks-and-service-discovery` — `content/stage-21/s21-networks-and-service-discovery/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.21.5.port-mapping` — `content/stage-21/s21-port-mapping/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.21.6.volumes` — `content/stage-21/s21-volumes/lesson.md`; новых закрытых блоков: 3.
- `backend-interview.22.7.conflict-resolution` — `content/stage-22/s22-conflict-resolution/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.22.10.gitignore-and-secrets` — `content/stage-22/s22-gitignore-and-secrets/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.22.12.practical-git-scenarios` — `content/stage-22/s22-practical-git-scenarios/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.22.6.rebase-basics` — `content/stage-22/s22-rebase-basics/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.22.9.reset-vs-revert` — `content/stage-22/s22-reset-vs-revert/lesson.md`; новых закрытых блоков: 2.
- `backend-interview.23.4.environment-variables` — `content/stage-23/s23-environment-variables/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.23.6.permissions` — `content/stage-23/s23-permissions/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.23.7.ports-and-network-diagnostics` — `content/stage-23/s23-ports-and-network-diagnostics/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.23.5.processes` — `content/stage-23/s23-processes/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.23.3.reading-searching-logs-and-files` — `content/stage-23/s23-reading-searching-logs-and-files/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.4.background-jobs` — `content/stage-29/s29-background-jobs/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.6.booking-endpoint` — `content/stage-29/s29-booking-endpoint/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.3.cache-placement` — `content/stage-29/s29-cache-placement/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.8.chat-websocket-design` — `content/stage-29/s29-chat-websocket-design/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.5.database-bottlenecks` — `content/stage-29/s29-database-bottlenecks/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.9.file-upload-design` — `content/stage-29/s29-file-upload-design/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.10.outbox-design` — `content/stage-29/s29-outbox-design/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.7.preventing-double-booking` — `content/stage-29/s29-preventing-double-booking/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.11.scaling-sequence` — `content/stage-29/s29-scaling-sequence/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.29.2.stateless-api-and-horizontal-scaling` — `content/stage-29/s29-stateless-api-and-horizontal-scaling/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.23.honest-boundaries` — `content/stage-32/s32-honest-boundaries/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.17.hotel-booking-and-double-booking` — `content/stage-32/s32-hotel-booking-and-double-booking/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.11.jwt-refresh-sessions` — `content/stage-32/s32-jwt-refresh-sessions/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.14.minio-and-presigned-urls` — `content/stage-32/s32-minio-and-presigned-urls/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.8.outbox-pattern` — `content/stage-32/s32-outbox-pattern/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.22.redis-backed-password-reset` — `content/stage-32/s32-redis-backed-password-reset/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.1.studyhub-in-60-seconds` — `content/stage-32/s32-studyhub-in-60-seconds/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.6.websockets-plus-redis-pub-sub` — `content/stage-32/s32-websockets-plus-redis-pub-sub/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.4.why-async` — `content/stage-32/s32-why-async/lesson.md`; новых закрытых блоков: 1.
- `backend-interview.32.5.why-postgresql-and-redis-together` — `content/stage-32/s32-why-postgresql-and-redis-together/lesson.md`; новых закрытых блоков: 1.
