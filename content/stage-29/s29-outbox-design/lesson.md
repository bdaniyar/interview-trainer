# Outbox design

## Суть

В system design outbox закрывает разрыв между локальным COMMIT business data и намерением сообщить об этом другому сервису. Он не объединяет две service DB в одну transaction.

## Учебные цели

Проследить booking и event intent в одной transaction, затем отдельную доставку в notification service. Проверить producer crash, потерянный ответ receiver, duplicate event и terminal failure relay.

## Зачем это нужно backend-разработчику

Запустите `scripts/test_architecture_lab.sh -k timeout`. Receiver успевает COMMIT, sender получает timeout, затем повторяет прежний event_id. Проверьте одну inbox/notification строку и delivered outbox после удачного ack.

## Теория

### Что это

В system design outbox закрывает разрыв между локальным COMMIT business data и намерением сообщить об этом другому сервису. Он не объединяет две service DB в одну transaction.

### Как работает

BookingService сохраняет outbox event рядом с booking. Relay получает короткий lease, COMMIT-ит claim, отправляет event и затем подтверждает delivery guarded generation. Это позволяет producer умереть после COMMIT без потери intent.

После receiver COMMIT и до ack возможен дубль. Notification service хранит event_id+hash и notification effect в своей transaction, поэтому одинаковый повтор не создаёт второй effect, а другой payload с тем же ID конфликтует. Дедупликация должна жить достаточно долго для допустимого replay.

Backlog age показывает задержку доставки лучше одного count: маленькая очередь может содержать одну очень старую poison event. Failed state после retry budget должен быть виден оператору. Повтор failed event сохраняет её ID; новый ID превращает retry в другую операцию.

Для payment события нужен provider_event_id и локальный ledger/transition с outbox. Это отдельный контракт; учебная notification не выполняет реальных платежей и не доказывает exactly-once у внешнего провайдера.

### Важный нюанс / ограничение

Outbox даёт durable intent и обычно at-least-once delivery. Один защищённый business effect требует receiver transaction и дедупликации на его стороне.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Событие имеет стабильный ID, version/schema, correlation и понятный business identity. Receiver объединяет inbox и effect своим COMMIT. Статус delivered означает подтверждённую доставку по конкретному контракту, а failed сохраняется для диагностики и безопасного операторского решения.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'timeout'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Отметить delivered до HTTP — потерять событие при crash. Создать новый event ID на каждом retry — обойти inbox. Принять прежний ID с изменённым payload — смешать разные события. Удалить inbox ради повторной отправки — разрешить второй business effect.

## Практика

Запустите `scripts/test_architecture_lab.sh -k timeout`. Receiver успевает COMMIT, sender получает timeout, затем повторяет прежний event_id. Проверьте одну inbox/notification строку и delivered outbox после удачного ack.

## Вопросы с собеседований

1. Почему нельзя отмечать delivered перед HTTP?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Падение после отметки до отправки потеряет событие. Отметка после отправки допускает повтор, который должен безопасно обработать receiver.

Outbox даёт durable intent и обычно at-least-once delivery. Один защищённый business effect требует receiver transaction и дедупликации на его стороне.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Запустите `scripts/test_architecture_lab.sh -k timeout`. Receiver успевает COMMIT, sender получает timeout, затем повторяет прежний event_id. Проверьте одну inbox/notification строку и delivered outbox после удачного ack.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Producer: business + outbox одним COMMIT. Relay: claim, отправка вне transaction, fenced ack. Consumer: inbox + effect одним COMMIT. Любая потеря ответа допускает повтор прежнего события. Между сервисами остаётся eventual consistency.

## Источники

- [PostgreSQL 17: transaction boundary](https://www.postgresql.org/docs/17/tutorial-transactions.html).
- [SQLAlchemy 2.0: transactions](https://docs.sqlalchemy.org/en/20/core/connections.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
