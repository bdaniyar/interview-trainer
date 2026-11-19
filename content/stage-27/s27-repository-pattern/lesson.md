# Repository pattern

## Суть

Repository даёт application code понятные операции хранения вместо разбросанных SQL-запросов. В нашем небольшом проекте BookingRepository содержит конкретные запросы бронирования, а не универсальный CRUD для всей системы.

## Учебные цели

Найти запросы, необходимые booking use case, и собрать их в осмысленные операции хранения. Сохранить общую транзакцию резерва, booking и intent; проверить её независимыми PostgreSQL-соединениями.

## Зачем это нужно backend-разработчику

Найдите reserve_one в `architecture/orders.py`. В своей копии замените conditional UPDATE на read/compute/write и добавьте синхронизацию двух чтений: double-booking test должен обнаружить проблему. Верните атомарную запись и запустите оба варианта workflow.

## Теория

### Что это

Repository даёт application code понятные операции хранения вместо разбросанных SQL-запросов. В нашем небольшом проекте BookingRepository содержит конкретные запросы бронирования, а не универсальный CRUD для всей системы.

### Как работает

Repository получает connection текущей transaction. insert использует unique request_key, existing проверяет повтор, reserve_one делает conditional UPDATE available>0 RETURNING. Application service решает, что эти операции должны COMMIT вместе с event intent.

SELECT-before-INSERT без unique constraint не защищает от двух запросов. Python method с названием reserve также не является lock: атомарность обеспечивает PostgreSQL statement/row lock и transaction. Repository не должен внутри каждого метода независимо COMMIT-ить, иначе частичный use case уже не откатить.

Оригинальный Repository pattern описывает collection-like доступ к domain objects. Наш класс — небольшой конкретный persistence adapter; в простой задаче это достаточно. Добавлять generic repository поверх каждого SQLAlchemy API не требуется, если он не уменьшает связанность.

### Важный нюанс / ограничение

Абстракция хранения не отменяет знание нужного concurrency contract. Fake in-memory repository не способен доказать поведение PostgreSQL при concurrent UPDATE.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Repository отражает нужды use case, а не все возможные CRUD-операции. Он получает connection текущей операции. Unique constraints и guarded UPDATE остаются частью корректности, даже если SQL скрыт за методом reserve.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'two_requests and orders'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Делать отдельный COMMIT в reserve и create_booking — оставлять списанный остаток без брони. Подменить конкурентный UPDATE чтением и записью Python-значения — открыть lost update. Добавить generic CRUD на все таблицы — скрыть бизнес-намерение и разрешить обход инвариантов.

## Практика

Найдите reserve_one в `architecture/orders.py`. В своей копии замените conditional UPDATE на read/compute/write и добавьте синхронизацию двух чтений: double-booking test должен обнаружить проблему. Верните атомарную запись и запустите оба варианта workflow.

## Вопросы с собеседований

1. Почему repository method не должен всегда сам делать COMMIT?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Несколько операций могут входить в один use case. Общая transaction boundary должна сохранить возможность отката reserve, booking и intent вместе.

Абстракция хранения не отменяет знание нужного concurrency contract. Fake in-memory repository не способен доказать поведение PostgreSQL при concurrent UPDATE.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Найдите reserve_one в `architecture/orders.py`. В своей копии замените conditional UPDATE на read/compute/write и добавьте синхронизацию двух чтений: double-booking test должен обнаружить проблему. Верните атомарную запись и запустите оба варианта workflow.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Repository именует операции хранения, use case связывает их одной транзакцией. Абстракция не отменяет constraints, isolation и locking. Поведение при гонке подтверждается реальной БД, а не in-memory fake.

## Источники

- [Fowler: Repository](https://martinfowler.com/eaaCatalog/repository.html).
- [PostgreSQL 17: row locking](https://www.postgresql.org/docs/17/explicit-locking.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
