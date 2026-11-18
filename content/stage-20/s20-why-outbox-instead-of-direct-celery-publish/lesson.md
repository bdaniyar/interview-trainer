# Why outbox instead of direct Celery publish

## Суть

Celery умеет доставить и исполнить задачу, но не объединяет publish в Redis с COMMIT вашей PostgreSQL-транзакции. Outbox и Celery решают разные части пути и могут использоваться вместе.

## Учебные цели

Разобрать обе очередности dual write: publish до COMMIT и после него. Объяснить оставшееся окно у after-commit callback и совместить durable outbox с существующим broker.

## Зачем это нужно backend-разработчику

Возьмите `deliver_once` из queue_app/outbox.py. Найдите три разные транзакции: producer, receiver, ack. Уберите receiver dedup в своей копии и повторите timeout-after-commit test: два эффекта покажут, почему одной Celery retry недостаточно.

## Теория

### Что это

Celery умеет доставить и исполнить задачу, но не объединяет publish в Redis с COMMIT вашей PostgreSQL-транзакции. Outbox и Celery решают разные части пути и могут использоваться вместе.

### Как работает

Publish before COMMIT допускает consumer, который не находит ещё не зафиксированный заказ, либо видит событие откатившейся операции. Publish after COMMIT оставляет окно потери при падении producer. Даже успешный producer confirm сообщает о принятии broker, а не об атомарности с business DB.

Правильная локальная граница — order/job + outbox в PostgreSQL. Relay может публиковать outbox event в Celery; task получает устойчивый event_id, consumer дедуплицирует эффект. Потеря ack после исполнения даёт повтор. В нашем проекте relay использует HTTP, чтобы явно увидеть этот же dual-write gap без магии framework.

Транзакционный on_commit callback решает раннюю публикацию, но callback в памяти всё ещё может потеряться после DB COMMIT. Устойчивость требует durable intent, а не только правильного порядка двух вызовов. Обсуждайте доступность и ручное восстановление failed events.

### Важный нюанс / ограничение

Outbox не требует заменить Celery своей очередью. Можно использовать Celery как delivery/execution layer, сохраняя DB intent и consumer idempotency. Нельзя заявлять distributed atomicity по одному факту наличия broker.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Ошибка публикации после успешного business COMMIT требует сохраняемого намерения, доступного другому процессу. Broker confirm полезен на транспортной границе, но не восстанавливает событие, которое producer вообще не успел отправить.

## Примеры кода

```python
stages = ["business+outbox COMMIT", "relay send", "receiver COMMIT", "relay ack"]
assert stages.index("receiver COMMIT") < stages.index("relay ack")
```

Это модель порядка str-меток, не concurrency proof. Настоящее доказательство даёт project test: receiver успел COMMIT, client получил timeout, повтор с тем же event_id не создаёт второй effect.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Publish перед COMMIT может породить событие о несуществующем заказе после rollback. Publish после COMMIT может не произойти при crash. Retry всего endpoint с новым ключом способен повторить сам заказ. After-commit hook меняет порядок, но не сохраняет неисполненный callback для другого процесса.

## Практика

Возьмите `deliver_once` из queue_app/outbox.py. Найдите три разные транзакции: producer, receiver, ack. Уберите receiver dedup в своей копии и повторите timeout-after-commit test: два эффекта покажут, почему одной Celery retry недостаточно.

## Вопросы с собеседований

1. Решает ли on_commit callback потерю publish?
2. Можно ли сочетать outbox и Celery?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Он не публикует до COMMIT, но process crash после COMMIT до callback всё ещё теряет событие. Durable outbox сохраняет intent.

Да. Outbox хранит локальный durable intent, relay публикует Celery task, consumer защищает business effect от повторов.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

Возьмите `deliver_once` из queue_app/outbox.py. Найдите три разные транзакции: producer, receiver, ack. Уберите receiver dedup в своей копии и повторите timeout-after-commit test: два эффекта покажут, почему одной Celery retry недостаточно.

Внесите изменение в свою копию проекта и запустите соответствующий integration test. Критерий успеха — сохранённый invariant и ожидаемый failure при намеренно сломанной границе; текстовое объяснение автоматически не оценивается.

## Шпаргалка

Dual write имеет два независимых результата. Outbox переносит атомарную часть в одну БД: business state + intent. Relay может публиковать через Celery; consumer по-прежнему обязан безопасно принимать повтор. Подтверждение broker не является общей DB/broker транзакцией.

## Источники

- [Celery 5.5.3: tasks / database transactions](https://docs.celeryq.dev/en/v5.5.3/userguide/tasks.html).
- [PostgreSQL 17: transaction tutorial](https://www.postgresql.org/docs/17/tutorial-transactions.html).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
