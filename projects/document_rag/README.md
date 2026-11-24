# P5 · Document Knowledge Assistant

Локальный FastAPI-сервис ищет в синтетических Markdown-документах и возвращает проверяемые ссылки на доступные текущие версии. Источник поиска — PostgreSQL 17 с pgvector и FTS. P5 переиспользует миграцию, контракты и хранилище [P4](../vector_search/README.md). Embeddings и генерация предсказуемы и работают без сервиса моделей.

## Запуск из корня репозитория

```sh
python3.12 -m venv .venv-rag
. .venv-rag/bin/activate
python -m pip install --require-hashes -r projects/document_rag/requirements.txt
VECTOR_PORT=15438 docker compose -f projects/document_rag/compose.yaml up -d --wait
python -m projects.document_rag.evaluate seed
python -m uvicorn projects.document_rag.main:app --host 127.0.0.1 --port 18766
```

Во втором терминале запусти `python -m projects.document_rag.smoke_http` из корня. Для запуска API в том же Compose вместо локального Uvicorn добавь `--profile api` и `--build` к команде `up`. Порт API на хосте задаёт `RAG_PORT` (18766). `VECTOR_PORT` должен оставаться 15438 для стандартных команд P5; при смене порта задай `VECTOR_DSN` для CLI и при необходимости `RAG_DSN`/ `RAG_TEST_DSN` для host API и тестов. PG слушает loopback, использует собственную роль и tmpfs. После остановки Postgres создавай корпус заново.

На свежей тестовой базе:
```sh
VECTOR_PORT=15440 docker compose -p pythoria-p5-tests -f projects/document_rag/compose.yaml up -d --wait
RAG_TEST_DSN=postgresql://vector_app:local_vector_app@127.0.0.1:15440/vector_lab \
VECTOR_DSN=postgresql://vector_app:local_vector_app@127.0.0.1:15440/vector_lab \
python -m pytest -o addopts='' -q projects/document_rag/tests
```

`python -m projects.document_rag.trace_demo` записывает безопасные локальные SDK spans. [Оценка](EVALUATION.md) содержит команды dev/holdout, а [данные](data) — результаты и измеренное время отдельно от детерминированных файлов.

## API

Передавай заголовок `X-Demo-Actor`. Пример `north-alice` выбирает объект приложения с tenant/subject/scopes. Учебный заголовок не проверяет настоящую личность. Сервер рассчитан на loopback.

| Маршрут | Контракт |
| --- | --- |
| `POST /documents` | `document_id`, положительный `version`, `markdown`; scope ingest. |
| `POST /documents/{id}/versions` | Новая `version` и `markdown`; владелец и ingest. |
| `POST /documents/{id}/acl` | `subject` того же tenant, `enabled`; владелец и share. |
| `DELETE /documents/{id}` | Владелец и delete. Ставит tombstone, повтор безопасен. |
| `POST /search` | `question`, опциональные `method` и `limit`; возвращает разрешённые citations без body. |
| `POST /ask` | Тот же запрос; результат с request ID, статусом, текстом, claims и citations, размером контекста и ревизиями. |

Методы: `fts`, `dense`, `hybrid`, `rerank`. По умолчанию exact dense, выбранный на dev. FTS нормализует запрос к учебному ключевому слову и использует `simple` словарь PostgreSQL. Dense использует фиксированные тематические признаки. RRF объединяет rank lists, reranker оценивает первые четыре доступных кандидата. ANN и его recall измеряются в P4.

## Поток и границы

```mermaid
flowchart LR
    API[FastAPI and trusted actor] --> I[Validate hash and chunk]
    I --> E[Scripted batch embed]
    E --> A[Atomic staging and activation]
    A --> DB[(PG17 pgvector and FTS)]
    API --> R[Authorized metadata retrieval]
    R --> DB
    R --> C[Scoped payload and bounded context]
    C --> G[Scripted generator]
    G --> V[Current ACL and source validation]
    V --> API
```

```mermaid
sequenceDiagram
    Caller->>API: ask(question)
    API->>DB: FTS / exact and ACL on active revision
    API->>DB: authorize and read selected payload
    API->>Provider: policy + bounded evidence
    Note over API,Provider: No open DB transaction while generating
    Provider-->>API: typed draft with source versions
    API->>DB: recheck all supplied references and epochs
    API-->>Caller: claims with citations or safe terminal status
```

См. [ADR и модель угроз](ADR.md) для границ read/write, конкурентности и trace. [Источники и версии](SOURCES.md).

## Защита проекта

Добавь регламент с новой версией и документ-приманку с похожим термином. Напиши тест, который находит активную версию, и отрицательный тест на идентичный ID другого tenant либо на отозванный grant. Сравни lexical/hybrid с одной разметкой и покажи по trace, пропал ли источник при retrieval, вышел ли из бюджета или был отклонён после генерации. Обоснуй, как воспроизвести тест после исправления.
