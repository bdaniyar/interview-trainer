# AI Engineering R3 · проверка выпуска

База `ea0bb67eba7c36d83b48c965d1cb7cf07d37b197`, R2 слит. В стеке R3 опубликованы 46 из 72 AI-уроков. AI1–AI6 содержат 4/10/8/7/7/10, AI7–AI10 запланированы. Всего 37 graded AI labs, 370 Backend-уроков и пять локальных проектов.

## Уроки и grading

Все строки published. Во всех есть самостоятельный offline Python Run/Check. Профиль V означает дополнительную работу с отдельной PostgreSQL, явно обозначенную в уроке. Полный task ID равен lesson ID с суффиксом `.practice`.

| Урок | Lesson ID | Task ID | Профиль | Hidden cases | Негативный контроль |
| --- | --- | --- | --- | ---: | --- |
| AI6.1 | `ai-engineering.06.01.cosine-similarity` | `ai-engineering.06.01.cosine-similarity.practice` | F | 17 | Абсолютное значение уничтожает знак cosine. |
| AI6.2 | `ai-engineering.06.02.embedding-pipeline` | `ai-engineering.06.02.embedding-pipeline.practice` | F | 15 | Принимается результат другой ревизии. |
| AI6.3 | `ai-engineering.06.03.chunking-and-provenance` | `ai-engineering.06.03.chunking-and-provenance.practice` | F | 13 | Убран overlap. |
| AI6.4 | `ai-engineering.06.04.pgvector-exact-search` | `ai-engineering.06.04.pgvector-exact-search.practice` | F + V | 12 | Отключена проверка owner/grant. |
| AI6.5 | `ai-engineering.06.05.ann-and-recall` | `ai-engineering.06.05.ann-and-recall.practice` | F + V | 16 | Recall делится на k при коротком эталоне. |
| AI6.6 | `ai-engineering.06.06.hybrid-and-rerank` | `ai-engineering.06.06.hybrid-and-rerank.practice` | F + V | 14 | Повторы получают отдельные RRF-голоса. |
| AI6.7 | `ai-engineering.06.07.plain-python-rag` | `ai-engineering.06.07.plain-python-rag.practice` | A | 15 | Retrieval заменён пустой константой. |
| AI6.8 | `ai-engineering.06.08.citations-and-abstention` | `ai-engineering.06.08.citations-and-abstention.practice` | F | 15 | Подходящая ссылка пропускается без support. |
| AI6.9 | `ai-engineering.06.09.rag-evaluation` | `ai-engineering.06.09.rag-evaluation.practice` | F | 10 | В recall подставляется k вместо размера qrels. |
| AI6.10 | `ai-engineering.06.10.document-rag-project` | `ai-engineering.06.10.document-rag-project.practice` | A + V | 13 | Убрана финальная проверка устаревшего evidence. |

Редакционная самопроверка Codex от 2026-11-24 по §15: 19/20 для AI6.1–6.5 и AI6.7–6.9, 18/20 для AI6.6 и AI6.10. Проверены источники, фактическая точность, последовательность, runnable code, публичный контракт, закрытые ответы, tests/feedback, конспекты и границы. В AI6.6 BM25 разобран на малом учебном корпусе, а сравнение FTS и dense вынесено в P5. В AI6.10 упражнение и реальные транзакции и трейсы разобраны отдельно. Наблюдаемые hard gates пройдены. Независимое ревью остаётся в открытых PR. Скрытые fixtures педагогические и синтетические.

## P4 · реальные планы и проверка exact

PostgreSQL 17.10, pgvector 0.8.2, psycopg 3.2.13. Образ native ARM64 закреплён по digest. Extension и grants исполняются доверенной миграцией, runtime роль без DDL. Две embedding spaces отделены партициями. Версии, ACL, tombstones и active pointer имеют составные связи. Семь интеграционных тестов подтверждают реальные привилегии, exact oracle, стабильные ничьи, tenant и owner, revoke, replay, ошибку до активации и идемпотентный параллельный ingest. [Архитектура P4](../projects/vector_search/README.md), [Qdrant ADR](../projects/vector_search/ADR_QDRANT.md).

Замер: Apple M3 ARM64, 16 GiB host и 7.654 GiB Docker VM, 3 840 векторов 16D, 2 304 разрешённых, seed 1305, 18 запросов, k=8, две незаписанные прогревочные пробы. HNSW индекс 1 433 600 bytes. `docker stats` после прогона показал 95.79 MiB у PG, измерение пика не выполнялось.

| План | ef_search | Recall@8 | Минимум результатов | p50 / p95, мс |
| --- | ---: | ---: | ---: | ---: |
| Exact, без HNSW | — | 1,0000 | 8 | 1,866 / 2,240 |
| Естественный HNSW | 16 | 0,9514 | 6 | 0,579 / 1,164 |
| Естественный HNSW | 48 | 1,0000 | 8 | 0,565 / 6,274 |
| Естественный HNSW | 128 | 1,0000 | 8 | 0,575 / 0,657 |

Forced планы, actual buffers/rows, параметры HNSW и формула p95 лежат в отдельном JSON. Показатели относятся к этому замеру. Qdrant сравнивался по документации, отдельный профиль не включён. [Измерения и EXPLAIN ANALYZE](../projects/vector_search/data/benchmark.json), [версии и источники](../projects/vector_search/SOURCES.md).

## P5 · реальные запросы и замороженная оценка

25 оригинальных документов, 26 Markdown-версий, два tenant. Для каждого из ru, kk и en — 6 dev и 4 holdout, всего 18/12. Переводы одного случая остаются в одном split. Corpus SHA-256 `31a18c57bc6e388a3a821ae86db9ef390e7c2c477bf5d49e4dc08550481d939f`. Exact dense с k=6 зафиксирован в `8ae02d6` после dev и до holdout. Все четыре retrieval метода сопоставлены на одних qrels и ACL.

| Метод | Dev recall / MRR (n=12) | Holdout recall / MRR (n=9) |
| --- | ---: | ---: |
| PostgreSQL FTS | 0,5833 / 0,9167 | 0,5185 / 0,6667 |
| Exact dense (выбран) | 1,0000 / 1,0000 | 1,0000 / 0,8333 |
| FTS + dense RRF | 1,0000 / 1,0000 | 1,0000 / 0,8333 |
| RRF + bounded rerank | 1,0000 / 1,0000 | 1,0000 / 1,0000 |

По языкам dev FTS recall (ru/kk/en) 0,500/0,250/1,000 при четырёх определённых cases на язык. Holdout FTS recall 0,444/0,111/1,000 при трёх на язык. Exact dense recall 1,000 во всех срезах. Ответы совпали по 6/6 dev и 4/4 holdout для каждого языка. Citation validity и claim support — по 9/9 определённых ответов в каждом split. Верные отказы 6/6 и 3/3. Верные конфликты 3/3 dev, для holdout метрика null. Неверные утверждения с формально допустимой ссылкой отклонены в 9/9 на каждом split. Forbidden/stale результатов **0** на всех методах. Отчёты совпали побайтово (SHA-256 dev `e26d8fff0ecbe6bda74880d9825b239cbfc4ddc94f7081b5b04730f750ba91a5`, holdout `647242e05b0754cf4263037525767aeb7fe07de31aa5e02835c4bd6665a20916`). Измеренное время отделено от eval: например, holdout dense 15,715 / 24,984 мс p50/p95, n=12.

Gold читает evaluator после генерации. Оценка охватывает scripted extractive replies, cross-language и code-switch. Независимой редакторской оценки kk и проверки качества live модели не было. [Корпус, split, метрики и ограничения](../projects/document_rag/EVALUATION.md).

Интеграции покрывают partial/replay, tenant/owner/scope, update/delete/revoke во время генерации, revoke→grant, повторное чтение без кэша, fabrication/injection и отрицательные контроли. Результат защищён в snapshot последней SQL-проверки. Более поздняя мутация может произойти до доставки ответа. Span tests проверяют parent/child, revisions, counts, error status и редактирование полей. Telemetry SDK 1.45.2 с локальным exporter. [ADR и границы](../projects/document_rag/ADR.md), [реальный безопасный trace](../projects/document_rag/data/redacted-trace.json), [источники](../projects/document_rag/SOURCES.md).

## Результаты проверок

| Команда | Фактический результат |
| --- | --- |
| `python3 -m pytest` | 323 passed. |
| `npm test`, `npm run lint`, `npx tsc --noEmit`, `npm run build` | 85 тестов, lint/typecheck/build прошли. Сборщик сообщил о размере чанков и классификации маршрута. |
| `python3 tools/validate_content.py --run-solutions` | 416 уроков, 105 executable tasks. Примеры и эталоны прошли. Аудит сообщает о 222 прежних Stage 8+ уроках с editorial debt. |
| `python3 scripts/smoke_ai_runtime.py --lesson AI6.1 … --lesson AI6.10` | 10 Run, 10 успешных Check, 140 hidden cases. Все 10 starter и 10 мутантов отклонены. Файлы сохранились. Повторный Check дал 0 XP. Sandbox блокирует внешний маршрут, доступ к основной БД и Docker socket. |
| `node scripts/smoke_sql_browser.mjs --ai-only` | 46 уроков через поиск, Learn/Review с закрытыми ответами, Markdown для AI6.10, глубокая ссылка, Monaco, save/reload, независимый прогресс, desktop/mobile 390 px и темы. Стартеры AI3.1 и AI6.10 отклонены, эталоны 11/11 и 13/13. Проверена публичная метка Python oracle для PG-урока. |
| `node scripts/smoke_sql_browser.mjs` | 23 SQL labs, 5 Worker labs, 3 Architecture-урока, Web Transaction Lab, JSONB и Index Lab. Проверены blocking/commit release, SQL draft и Python files после reload, отдельный прогресс и XP. |
| `SQL_DOCKER_TESTS=1 python3 -m pytest -o addopts='' -q sql_runner/tests/integration/test_postgres.py` | 19 passed с настоящим ограниченным PostgreSQL. |
| `python -m pytest -o addopts='' -q projects/vector_search/tests` и та же команда для `projects/document_rag/tests` | P4 7, P5 16. Отдельные PG профили. |
| `python -m projects.document_rag.smoke_http` | Прошёл через host Uvicorn и через свежий Compose-профиль `api`. Подтверждены казахский вопрос с цитатой, tenant, отказ на подмене поля, replay и tombstone. Docker-образ собран с закреплённым uv и хешами lock. |
| Тесты P1, P2, P3 и `python -m pytest -o addopts='' -q tools/ai_sdk_verify` | 26/33/33 и 22 MockTransport. |

## Совместимость и границы

`test_expansion_preserves_synthetic_progress_and_files` переключает 15→29, 29→36 и 36→46 на disposable SQLite. Сверяет saved files, AI/Backend progress, interview, XP, тему и навигацию. Новые записи остаются незавершёнными. Tree diff подтвердил сохранение 36 прежних AI bundles, 370 Backend-уроков, SQL registrations и grader bundles, Backend, Frontend и Runner runtime, Compose основной системы и P1–P3. Браузерный прогон использовал отдельный tmpfs SQLite и изолированные PG services. Основное хранилище и сборка Pythoria не менялись.

R3 использует локальные fixtures без модельных загрузок, GPU или платного API. Сравнение Qdrant ограничено ADR. Browser Check работает только в существующей Python-песочнице. Результаты независимого проекта P5 оценивают контракт приложения.

## Ручная интеграция

| Этап | PR | Исходная base | Проверки по поставке |
| --- | --- | --- | --- |
| 13A | [#36](https://github.com/bdaniyar/interview-trainer/pull/36) | `main` | Три offline labs, 45 сценариев, 8 manifest checks. |
| 13B | [#37](https://github.com/bdaniyar/interview-trainer/pull/37) | `feat/ai-embedding-foundations-phase13a` | Два offline labs, 28 сценариев, 7 PG интеграций, exact/HNSW benchmark. |
| 13C | [#38](https://github.com/bdaniyar/interview-trainer/pull/38) | `feat/ai-pgvector-search-phase13b` | Два offline labs, 29 сценариев, FTS/hybrid и scoped recheck. |
| 13D | [#39](https://github.com/bdaniyar/interview-trainer/pull/39) | `feat/ai-hybrid-rag-phase13c` | Два offline labs, 25 сценариев, замороженные dev/holdout. |
| 13E | [#40](https://github.com/bdaniyar/interview-trainer/pull/40) | `feat/ai-citations-evaluation-phase13d` | AI6.10, 13 сценариев, P5 HTTP/OTel, итоговые проверки. |

Порядок merge commits **#36 → #37 → #38 → #39 → #40**. После каждого слияния перевести base следующего на `main` и сверить diff. Этот порядок сохраняет границы ревью. Автоматических merge и force-push не было.
