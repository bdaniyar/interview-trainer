# P4 · PostgreSQL Vector Search

Учебный проект с настоящим PostgreSQL 17 и pgvector. Браузерные AI6.4/AI6.5 проверяют oracle и метрики на Python. Эта отдельная практика проверяет планы, права и транзакции.

## Запуск из корня репозитория

```sh
python3.12 -m venv .venv-vector
. .venv-vector/bin/activate
python -m pip install --require-hashes -r projects/vector_search/requirements.txt
docker compose -f projects/vector_search/compose.yaml up -d --wait
python -m projects.vector_search.cli seed
python -m projects.vector_search.cli exact
python -m projects.vector_search.cli ann
python -m pytest -o addopts='' -q projects/vector_search/tests
```

PG слушает loopback на 15437. Параметры локального runtime находятся в `cli.py`, адрес отдельного экземпляра можно задать через `VECTOR_DSN`. Синтетический пароль нужен только для одноразовой локальной базы. Образ закреплён по digest multiarch тега. Инициализация с пустого tmpfs последовательно выполняет SQL под `vector_admin`; дополнительная таблица с правами или расширение не устанавливаются из студенческого Runner. Остановка/пересоздание PostgreSQL стирает данные tmpfs.

## Схема и семантика

```mermaid
flowchart LR
    T[tenant] --> D[document and ACL]
    D --> V[version and space identity]
    V --> C[chunk vector and source offsets]
    C --> P[protected text payload]
    D -. active version and access epoch .-> V
```

Каждый document key включает tenant. Версия содержит fingerprint содержимого, число фрагментов и embedding space. Две партиции физически разделяют два пространства одной размерности, а составные foreign keys сохраняют связь версии, space и chunk. Payload хранится отдельно от проекции retrieval. Роль runtime имеет доступ к нужному DML, без CREATE и DDL. Предикаты приложения являются границей доступа к документам в локальном демо.

Embedding передаётся уже подготовленным. Ingest проверяет конечность, единичную норму, форму и покрытие фрагментов. Транзакция блокирует запись документа, вставляет версию и все фрагменты с payload, затем переключает `active_version`. При rollback читатели продолжают видеть старый snapshot. Повтор той же версии и fingerprint идемпотентен, а другая версия с тем же номером конфликтует. Grant, revoke, delete и activate сериализуются по document row lock. Tombstone запрещает повторную активацию и исключает документ из выдачи, при этом исторические строки остаются в учебной БД.

Exact материализует разрешённые записи и затем сортирует cosine distance с tie-break по document/chunk ID. ANN даёт оптимизатору возможность пройти HNSW; фильтры owner/grant, active version, tenant, tombstone и space применяются до LIMIT, но pgvector может посетить недостаточно соседей после фильтрации. Для равных значений по разные стороны ANN cut-off порядок гарантирован только внутри возвращённого набора. [ADR сравнения pgvector и Qdrant](ADR_QDRANT.md).

## Измерение

Запускайте отдельно от seed и integration tests, в новом проекте на другом порту:

```sh
VECTOR_PORT=15439 docker compose -p pythoria-p4-measure -f projects/vector_search/compose.yaml up -d --wait
VECTOR_DSN=postgresql://vector_app:local_vector_app@127.0.0.1:15439/vector_lab \
VECTOR_BENCH_ADMIN_DSN=postgresql://vector_admin:local_vector_admin@127.0.0.1:15439/vector_lab \
  python -m projects.vector_search.cli benchmark --output /tmp/p4-benchmark.json
docker compose -p pythoria-p4-measure -f projects/vector_search/compose.yaml down
```

18 запросов, seed 1305, размерность 16, 3 840 строк и 2 304 разрешённых фрагмента, k=8. После ANALYZE и двух незаписанных прогревочных запросов статистика измеряется на стороне клиента, p95 — inclusive quantile. В отчёте хранятся планы EXPLAIN ANALYZE с буферами, статистика и выбор индексов. Exact не использовал HNSW. Естественный ANN выбрал `chunks_v1_hnsw` при ef_search 16/48/128. В этом запуске recall@8 был 0.9514/1.0000/1.0000. На ef=16 один запрос вернул только 6 фрагментов. Forced режим записан отдельно. Значения времени относятся к этому запуску и оборудованию. [Измеренный JSON](data/benchmark.json).

## Защита

Измени фильтр разрешённых версий так, чтобы учитывалась добавленная метка владения. Добавь тест для чужой метки и сравни exact ID, естественный HNSW plan и recall на одинаковой доступной выборке. Объясни, почему assertion для top-k прошёл с данными владельца и сломался бы при переносе filtering после LIMIT.
