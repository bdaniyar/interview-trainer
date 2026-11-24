# P4 · источники и версии

Проверено 2026-11-24. PostgreSQL 17.10 и pgvector 0.8.2 измерены в native ARM64 контейнере. Psycopg 3.2.13 с binary package и pytest 8.4.1 установлены по хешам. CPython 3.12.13. Apple M3, модель Mac15,12, 16 GiB памяти, Docker VM показывала 7.654 GiB лимита. После benchmark `docker stats --no-stream` показал 95.79 MiB для PostgreSQL. Это наблюдение после нагрузки, без оценки пиков.

- Операторы distance, индекс HNSW, m/ef_construction/ef_search и filters. [pgvector 0.8.2](https://github.com/pgvector/pgvector/tree/v0.8.2)
- Навигация по слоям графа. [Malkov и Yashunin, HNSW](https://arxiv.org/abs/1603.09320)
- EXPLAIN, actual time, rows и buffers. [PostgreSQL 17](https://www.postgresql.org/docs/17/using-explain.html)
- Отдельная отправка SQL и параметров. [Psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html)
- Collections, filters, snapshots и tenant partitioning описаны в [ADR](ADR_QDRANT.md). Сравнение архитектур опирается на документацию, а измерения в benchmark относятся к PostgreSQL.
