# Stateless API and horizontal scaling

## Суть

Stateless API не хранит единственную правду о пользователе или заказе в памяти конкретного процесса. Следующий запрос может попасть на другую replica и получить корректный ответ из устойчивого хранилища.

## Учебные цели

Отправить запросы к двум независимым API processes и получить общий корректный результат. Найти состояние, которое нельзя оставить единственной копией в памяти replica, и оценить суммарный connection budget.

## Зачем это нужно backend-разработчику

Запустите `scripts/test_architecture_lab.sh -k stateless`. Два настоящих API process получают одинаковый key одновременно; ожидаются один 201, один 200 и один booking. Каждый процесс должен прочитать тот же UUID.

## Теория

### Что это

Stateless API не хранит единственную правду о пользователе или заказе в памяти конкретного процесса. Следующий запрос может попасть на другую replica и получить корректный ответ из устойчивого хранилища.

### Как работает

Booking state, availability, idempotency keys и notification intents находятся в PostgreSQL. Два instances могут одновременно обрабатывать POST: unique constraint и conditional UPDATE согласуют их независимо от process-local памяти.

Stateless не означает «нет состояния нигде» и не обещает неограниченное scaling. База, connection pool, downstream и CPU остаются ограниченными ресурсами. Если каждая replica открывает pool 10, сто replicas могут запросить тысячу connections. Нужны общий budget, backpressure и измерение bottleneck.

In-memory cache/lock может ускорить локальную работу, но не должен быть единственной защитой inventory. Sticky sessions маскируют эту зависимость до restart или rebalance. Lease worker и durable idempotency переживают смену процесса; локальный mutex — нет.

### Важный нюанс / ограничение

Horizontal scaling увеличивает число исполнителей, а не автоматически capacity БД. Сначала сохраните shared invariants, затем измерьте реальные ограничения.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Реплики должны видеть одну устойчивую истину и одинаковый idempotency ledger. Process-local lock не синхронизирует разные workers. Число replicas умножает размер connection pools и downstream concurrency; балансировщик не устраняет эти ограничения.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'stateless'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Дедуплицировать запросы только dict в памяти — разрешить дубль через другую replica. Хранить нужный следующему запросу файл только в локальном container filesystem — привязать клиента к одному экземпляру. Добавлять replicas без общего DB pool budget — перегрузить БД раньше роста полезной пропускной способности.

## Практика

Запустите `scripts/test_architecture_lab.sh -k stateless`. Два настоящих API process получают одинаковый key одновременно; ожидаются один 201, один 200 и один booking. Каждый процесс должен прочитать тот же UUID.

## Вопросы с собеседований

1. Почему mutex внутри одного API process не предотвращает double booking между replicas?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

У каждого процесса своя память и lock. Общий invariant должен защищаться на общей устойчивой границе, например атомарной PostgreSQL-транзакцией.

Horizontal scaling увеличивает число исполнителей, а не автоматически capacity БД. Сначала сохраните shared invariants, затем измерьте реальные ограничения.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Запустите `scripts/test_architecture_lab.sh -k stateless`. Два настоящих API process получают одинаковый key одновременно; ожидаются один 201, один 200 и один booking. Каждый процесс должен прочитать тот же UUID.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Любая replica может обслужить следующий запрос. Durable business state и unique keys общие; локальная память — лишь необязательный cache. Ограничивайте суммарные connections и inflight. Корректность двух processes проверяется до измерения масштабирования.

## Источники

- [PostgreSQL 17: explicit locks](https://www.postgresql.org/docs/17/explicit-locking.html).
- [Docker Compose: service networking](https://docs.docker.com/compose/how-tos/networking/).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
