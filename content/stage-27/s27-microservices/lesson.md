# Microservices

## Суть

Микросервис — самостоятельно разворачиваемая часть системы вокруг определённой бизнес-возможности, с явным контрактом и владением своими данными. Несколько контейнеров с общими внутренними таблицами ещё не дают такую независимость.

## Учебные цели

Сравнить две версии booking workflow по владению данными, deployment и поведению при отказе. Проследить event через outbox/HTTP/inbox и объяснить, почему независимые COMMIT допускают временно разные состояния сервисов.

## Зачем это нужно backend-разработчику

Запустите `scripts/test_architecture_lab.sh`. Найдите actual failures: unavailable service, timeout-after-COMMIT, duplicate event, producer crash, consumer restart и stale read. Для каждого выпишите состояния обеих БД и event_id. Объясните, почему COMMIT booking не откатывается из-за поздней notification ошибки.

## Теория

### Что это

Микросервис — самостоятельно разворачиваемая часть системы вокруг определённой бизнес-возможности, с явным контрактом и владением своими данными. Несколько контейнеров с общими внутренними таблицами ещё не дают такую независимость.

### Как работает

В project booking service владеет inventory/bookings/outbox, notification service — inbox/notifications. У каждого отдельная БД и роль, чужой CONNECT запрещён. Один PostgreSQL cluster экономит ресурсы учебного стенда, но остаётся общим failure domain. Независимое владение не означает, что разрешено делать cross-DB join чужой schema.

Sync HTTP требует известного API: метод/path, JSON schema, status codes, deadline и совместимость версий. Async event сообщает о факте и допускает отставание consumer. Здесь relay отправляет HTTP event после booking COMMIT. Service discovery в Compose идёт по DNS service name notifications, а не по постоянному IP контейнера; в другом deployment нужен соответствующий discovery mechanism.

Сеть добавляет partial failure: booking уже COMMIT, notification недоступен; receiver уже COMMIT, response потерялся. Timeout ограничивает ожидание, но не доказывает отсутствие эффекта. Повтор использует устойчивый event_id; inbox и effect фиксируются вместе. Outbox сохраняет intent producer, но не делает две БД одной транзакцией.

Eventual consistency означает, что notification read может сначала вернуть 404, а позже запись. Нужно объяснить клиенту промежуточное состояние и продумать reconciliation/failed handling. Saga координирует последовательность локальных операций и явных компенсаций; refund или release reservation — новые business actions, которые тоже могут ошибиться. В проекте нет скрытой distributed rollback и production payment saga.

Независимый deployment требует совместимого контракта: сначала добавить необязательное поле/поддержку, затем обновить consumers; удаление поля может потребовать новую версию. Отдельный process restart в тесте проверяет durable state, но не заменяет pipeline, rollback и schema migration strategy.

Observability связывает запрос, outbox event и receiver по correlation ID. Полноценный distributed trace дополнительно содержит spans, parent-child связи, propagation и sampling. В стенде есть JSON logs/correlation, но OTel collector и trace backend не развёрнуты. Нужно наблюдать error rate, latency, queue lag и saturation, а не только health=200.

### Важный нюанс / ограничение

Микросервисы добавляют независимые releases и ownership, но увеличивают operational cost, сетевые ошибки и сложность тестов. Для этого небольшого workflow modular monolith — разумная исходная версия; выделение сервиса требует конкретной причины.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Нужны явный владелец данных, совместимый API, deadline, retry policy и механизм наблюдения. Timeout может скрывать уже сохранённый результат. Независимость release ограничена совместимостью контрактов и миграций; общий PostgreSQL cluster остаётся общей точкой отказа.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'distributed or unavailable'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Дать сервисам общие внутренние таблицы — связать независимые releases через schema. Автоматически повторять HTTP с новым operation ID — допустить дубль. Обещать rollback чужого COMMIT — скрыть необходимость компенсации. Называть correlation ID полноценным trace — потерять spans, propagation и причинные связи.

## Практика

Запустите `scripts/test_architecture_lab.sh`. Найдите actual failures: unavailable service, timeout-after-COMMIT, duplicate event, producer crash, consumer restart и stale read. Для каждого выпишите состояния обеих БД и event_id. Объясните, почему COMMIT booking не откатывается из-за поздней notification ошибки.

## Вопросы с собеседований

1. Что отличает микросервис от отдельной папки или контейнера?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Самостоятельный deployable вокруг business capability, явный внешний контракт и собственное владение данными. Это сопровождается сетевыми отказами, независимыми транзакциями и operational responsibility.

Микросервисы добавляют независимые releases и ownership, но увеличивают operational cost, сетевые ошибки и сложность тестов. Для этого небольшого workflow modular monolith — разумная исходная версия; выделение сервиса требует конкретной причины.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Запустите `scripts/test_architecture_lab.sh`. Найдите actual failures: unavailable service, timeout-after-COMMIT, duplicate event, producer crash, consumer restart и stale read. Для каждого выпишите состояния обеих БД и event_id. Объясните, почему COMMIT booking не откатывается из-за поздней notification ошибки.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Граница сервиса объединяет бизнес-ответственность, владение данными и самостоятельный release. Сеть приносит partial failure. Outbox хранит intent, inbox дедуплицирует delivery, saga задаёт отдельные компенсации. Выделение сервиса должно оправдывать дополнительные эксплуатационные расходы.

## Источники

- [Lewis/Fowler 2014: Microservices](https://martinfowler.com/articles/microservices.html).
- [Docker Compose: service discovery](https://docs.docker.com/compose/how-tos/networking/).
- [OpenTelemetry: traces](https://opentelemetry.io/docs/concepts/signals/traces/).
- [Saga: local transactions and compensation](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
