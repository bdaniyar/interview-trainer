# ADR · хранилище для P4 и P5

Принято 2026-11-24. Основное хранилище — PostgreSQL 17 + pgvector. Версии, ACL, tombstone и тексты уже выражены в SQL, поэтому их можно обновить одной транзакцией.

| Вопрос | PostgreSQL + pgvector | Qdrant |
| --- | --- | --- |
| Данные поиска | Партиции по embedding space, vector и FTS рядом с relational metadata | Collections и points, named dense/sparse vectors, payload и индексы полей |
| Tenant и ACL | Составные ключи и join по tenant/document, owner/grants в запросе | Обязательные payload filters и tenant-aware индекс или отдельная collection для нужной границы; доступ приложения проверяется независимо |
| Обновление версии | Документ и chunks переключаются одной транзакцией | Upsert/delete имеют свои гарантии. Связь с внешней SQL версией требует outbox/reconciliation, видимость до подтверждения нужно определить |
| Revoke / delete | Отбор видит активную версию, актуальное grant и tombstone | Перенести метаданные доступа в payload и фильтровать по актуальной версии. До подтверждения индекса обращаться к авторитетной ACL, отслеживать запаздывание, повторять идемпотентно |
| Резервная копия | База и метаданные совместно в SQL backup, отдельно проверяем restore | Snapshots коллекций и согласованное восстановление базы ACL, векторов и метаданных |
| Эксплуатация | Одна БД, нагрузка FTS/index конкурирует с SQL | Отдельный процесс, память, snapshots, интеграция и мониторинг репликации данных |

Рассматривать Qdrant имеет смысл при отдельно измеренной потребности в vector workloads или sparse/dense API. Дополнительный профиль не входит в запуск R3. При сравнении зафиксировать те же IDs, векторы, qrels, k и eligible filters. Сравнивать recall и p50/p95, после revoke/delete проверять доступность с тем же principal. API и модель данных сверены с документацией. Производительность и совместимость живого Qdrant в этом проекте не измерялись. [Filtering](https://qdrant.tech/documentation/search/filtering/), [Snapshots](https://qdrant.tech/documentation/concepts/snapshots/), [Multitenancy](https://qdrant.tech/documentation/guides/multiple-partitions/).
