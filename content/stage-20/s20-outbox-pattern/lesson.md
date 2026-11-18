# Outbox pattern

## Суть

После COMMIT заказа нужно отправить событие. Если процесс умрёт между COMMIT и publish, событие потеряется. Если publish сделать раньше COMMIT, consumer может увидеть событие заказа, который затем откатился.

## Учебные цели

Сохранить бизнес-изменение вместе с намерением отправить событие. Проследить relay после падения producer и повтор после неизвестного HTTP-результата, не обещая общей транзакции двух систем.

## Зачем это нужно backend-разработчику

Для события `event-42` нарисуйте три точки падения: до COMMIT, после COMMIT до send, после receiver COMMIT до ack. Для каждой назовите состояние job/outbox/receiver. Запустите реальные outbox tests, затем в копии перенесите INSERT outbox за границу транзакции: rollback test должен обнаружить разрыв.

## Теория

### Что это

После COMMIT заказа нужно отправить событие. Если процесс умрёт между COMMIT и publish, событие потеряется. Если publish сделать раньше COMMIT, consumer может увидеть событие заказа, который затем откатился.

### Как работает

Outbox помещает business row и event row в одну локальную DB-транзакцию. После COMMIT отдельный relay выбирает недоставленные события, отправляет и отмечает результат. Если producer падает, строки остаются; если транзакция откатывается, не остаётся ни job, ни события.

Отметить delivered и отправить HTTP атомарно обычной PostgreSQL-транзакцией нельзя. Relay может получить успешный response и умереть до ack: следующий relay отправит дубль. Поэтому event_id стабилен, а receiver хранит inbox/dedup ledger вместе со своим business effect. В проекте claim_event и ack_event fenced generation защищают от старого relay.

Не удерживайте DB transaction через remote call: это долго держит locks и соединения, но не устраняет неизвестный исход HTTP. Сначала короткий claim COMMIT, затем send, затем короткий guarded ack. Outbox требует наблюдения за backlog, age, retry и poison events.

### Важный нюанс / ограничение

Outbox обеспечивает атомарность записи intent с локальным бизнес-состоянием. Доставка обычно at-least-once, внешний эффект требует собственного idempotency contract. Удаление outbox до подтверждения может потерять событие.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Relay берёт durable intent, освобождает транзакцию перед сетью и подтверждает доставку отдельно. Event ID сохраняется между повторами. Lease/generation защищают состояние relay, а inbox/unique business key — состояние receiver; это разные guards.

## Примеры кода

```sh
docker compose -f projects/durable_queue/compose.test.yml run --rm tests pytest -q -p no:cacheprovider tests -k outbox
```

Сначала соберите test image и поднимите зависимости через scripts/test_durable_queue.sh. Тесты внедряют сбой между INSERT job и outbox и после их COMMIT. Ожидание: rollback оставляет 0 jobs/0 events; committed job остаётся с доступным событием для другого relay.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Создать outbox после отдельного COMMIT заказа — снова открыть окно потери. Удалить intent до отправки — потерять его при crash. Создать новый event ID на retry — обойти inbox. Держать row lock во время HTTP — связать доступность БД с медленным downstream.

## Практика

Для события `event-42` нарисуйте три точки падения: до COMMIT, после COMMIT до send, после receiver COMMIT до ack. Для каждой назовите состояние job/outbox/receiver. Запустите реальные outbox tests, затем в копии перенесите INSERT outbox за границу транзакции: rollback test должен обнаружить разрыв.

## Вопросы с собеседований

1. Что атомарно гарантирует outbox?
2. Почему receiver всё равно должен дедуплицировать?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Business row и event intent фиксируются вместе в одной БД. Сам remote publish в эту транзакцию не входит.

Relay может умереть после remote success до локального ack. Повтор того же event_id должен дать один business effect.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

Для события `event-42` нарисуйте три точки падения: до COMMIT, после COMMIT до send, после receiver COMMIT до ack. Для каждой назовите состояние job/outbox/receiver. Запустите реальные outbox tests, затем в копии перенесите INSERT outbox за границу транзакции: rollback test должен обнаружить разрыв.

Внесите изменение в свою копию проекта и запустите соответствующий integration test. Критерий успеха — сохранённый invariant и ожидаемый failure при намеренно сломанной границе; текстовое объяснение автоматически не оценивается.

## Шпаргалка

Business row + intent — один COMMIT. Claim intent, HTTP и ack — отдельные шаги. Crash между ними может вызвать повтор, поэтому event ID стабилен и receiver дедуплицирует эффект. Следите за возрастом pending intent и terminal failures, а не только за числом отправок.

## Источники

- [PostgreSQL 17: transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html).
- [SQLAlchemy 2.0: Engine.begin](https://docs.sqlalchemy.org/en/20/core/connections.html#connect-and-begin-once-from-the-engine).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
