# Layered architecture

## Суть

Layered architecture организует путь HTTP → application use case → persistence. Слои помогают локализовать знания: endpoint понимает HTTP, repository — SQL, service — порядок бизнес-операций.

## Учебные цели

Проследить запрос через endpoint, application service и repository. Определить, кто валидирует HTTP, кто задаёт порядок бизнес-операций и кто владеет началом и завершением транзакции.

## Зачем это нужно backend-разработчику

Проследите `POST /bookings` до COMMIT и выпишите четыре роли компонентов. В копии вставьте ошибку after_record: rollback test должен сохранить исходный available=1. Проверьте, что relay HTTP выполняется без открытой booking transaction.

## Теория

### Что это

Layered architecture организует путь HTTP → application use case → persistence. Слои помогают локализовать знания: endpoint понимает HTTP, repository — SQL, service — порядок бизнес-операций.

### Как работает

В учебном workflow Pydantic Booking валидирует форму запроса, BookingService.place открывает transaction, BookingRepository резервирует inventory и сохраняет booking. Adapter записывает notification intent. Ошибка до выхода из engine.begin откатывает локальную работу.

Направление зависимостей не становится идеальным только от названий файлов. Наш service использует SQLAlchemy connection, поэтому это прагматичный layered example, а не полностью независимая domain model. Следующий шаг при росте сложности — явный UnitOfWork port и domain types, если они уменьшают реальные зависимости.

ORM entity, HTTP DTO и domain invariant имеют разное назначение. Не возвращайте lazy ORM graph после закрытия session и не открывайте transaction на всё время внешнего HTTP. Большой generic service часто скрывает несколько независимых use cases.

### Важный нюанс / ограничение

Слой полезен, когда отделяет знание и ответственность. Локальная DB transaction не должна незаметно продолжаться через remote call, даже если вызов спрятан за красивым adapter.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Endpoint переводит HTTP в вызов use case и результат обратно в status/body. Service определяет бизнес-операцию; repository выполняет запросы. Транзакция охватывает весь нужный invariant, а не обязательно один метод хранения.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'monolith or distributed_producer_rollback'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Поместить всё правило последнего места в endpoint — привязать бизнес-операцию к HTTP. Отдать COMMIT каждому repository method — разбить атомарную операцию. Спрятать remote HTTP внутри метода save — сделать задержку и частичный отказ неожиданными для вызывающего кода.

## Практика

Проследите `POST /bookings` до COMMIT и выпишите четыре роли компонентов. В копии вставьте ошибку after_record: rollback test должен сохранить исходный available=1. Проверьте, что relay HTTP выполняется без открытой booking transaction.

## Вопросы с собеседований

1. Почему один repository на каждую таблицу не определяет хорошую архитектуру?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Нужны границы use case и согласованных invariants. Набор CRUD wrappers сам по себе не задаёт transaction boundary и может размазать бизнес-операцию.

Слой полезен, когда отделяет знание и ответственность. Локальная DB transaction не должна незаметно продолжаться через remote call, даже если вызов спрятан за красивым adapter.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Проследите `POST /bookings` до COMMIT и выпишите четыре роли компонентов. В копии вставьте ошибку after_record: rollback test должен сохранить исходный available=1. Проверьте, что relay HTTP выполняется без открытой booking transaction.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

HTTP layer знает протокол; use case знает цель и порядок; persistence знает SQL. Composition root связывает реализации. Границы слоёв помогают видеть transaction boundary, но не создают её сами.

## Источники

- [SQLAlchemy 2.0: connection/transaction lifetime](https://docs.sqlalchemy.org/en/20/core/connections.html).
- [Cockburn: application boundary](https://alistair.cockburn.us/hexagonal-architecture).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
