# Kafka basics

## Суть

Kafka хранит append-only log в topic partitions. Consumer читает records по offset; чтение не удаляет запись немедленно. Другой consumer group может перечитать сохранённый log независимо.

## Учебные цели

Прочитать сохранённый log двумя независимыми consumer groups. Объяснить partition order, offset и последствия commit до или после внешнего эффекта.

## Зачем это нужно backend-разработчику

В manual lab создайте topic с 2 partitions, направьте по два records в каждую и прочитайте offsets. Объясните, почему нельзя требовать глобальный порядок четырёх сообщений без дополнительного протокола. Для автоматической проверки сначала сохраните детерминированный single-partition smoke.

## Теория

### Что это

Kafka хранит append-only log в topic partitions. Consumer читает records по offset; чтение не удаляет запись немедленно. Другой consumer group может перечитать сохранённый log независимо.

### Как работает

Partition задаёт локальный порядок offsets. Между несколькими partitions общего порядка нет. Внутри consumer group partition назначается одному consumer в данный момент; добавление consumer сверх числа partitions не увеличивает параллелизм чтения этого topic. Rebalance меняет ownership и требует корректной обработки inflight work.

Offset commit означает позицию, с которой group продолжит чтение. Commit до business effect допускает потерю работы; после эффекта допускает повтор при падении. Kafka transaction может объединить операции внутри поддерживаемой Kafka boundary, но не произвольный COMMIT в вашей PostgreSQL автоматически. Внешний consumer всё равно должен определить idempotency/transaction boundary.

Retention определяет, сколько log доступен для replay; это не бесконечный архив. Key влияет на partitioning при выбранном producer partitioner, а не обещает порядок всех пользователей во всём topic. Работайте с schema/compatibility и lag как отдельными контрактами.

### Важный нюанс / ограничение

Лаборатория использует одну partition и два consumer groups: она доказывает retained replay и порядок этих двух records. Она не тестирует replicated cluster, rebalance или Kafka exactly-once transactions.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Topic состоит из partitions; порядок определяется внутри partition. Group распределяет partitions между consumers и хранит своё положение чтения. Чтение не удаляет запись: retention и compaction имеют отдельные правила. Commit offset не включает транзакцию PostgreSQL.

## Примеры кода

```sh
python3 projects/durable_queue/check_kafka.py
```

Kafka CLI создаёт уникальный topic с одной partition, producer отправляет first и second. Group A и независимая group B с --from-beginning и --max-messages 2 получают ровно эти две строки в том же порядке. JSON kafka_retained_replay=true печатается только после обоих сравнений.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Требовать общий порядок разных partitions без дополнительного протокола — неверный контракт. Commit offset до обработки допускает пропуск при падении; после обработки — повтор. Запускать больше активных consumers, чем partitions в group, не увеличивает число одновременно назначенных partitions.

## Практика

В manual lab создайте topic с 2 partitions, направьте по два records в каждую и прочитайте offsets. Объясните, почему нельзя требовать глобальный порядок четырёх сообщений без дополнительного протокола. Для автоматической проверки сначала сохраните детерминированный single-partition smoke.

## Вопросы с собеседований

1. Чем consumer group отличается от отдельной очереди для каждого читателя?
2. Делает ли offset commit внешний SQL effect атомарным?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Group распределяет partition ownership и offsets; другая group может независимо читать тот же retained log.

Нет. Нужно определить границу consumer business transaction и дедупликацию; Kafka offset не является частью обычной PostgreSQL-транзакции.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

В manual lab создайте topic с 2 partitions, направьте по два records в каждую и прочитайте offsets. Объясните, почему нельзя требовать глобальный порядок четырёх сообщений без дополнительного протокола. Для автоматической проверки сначала сохраните детерминированный single-partition smoke.

Внесите изменение в свою копию проекта и запустите соответствующий integration test. Критерий успеха — сохранённый invariant и ожидаемый failure при намеренно сломанной границе; текстовое объяснение автоматически не оценивается.

## Шпаргалка

Partition определяет порядок, group — независимое потребление, offset — положение чтения. Запись остаётся в log по правилам retention. Для внешней БД отдельно проектируются transaction boundary и дедупликация. Учебный single-partition replay не проверяет rebalance и отказ кластера.

## Источники

- [Kafka 4.1: quickstart / consume and retained records](https://kafka.apache.org/41/getting-started/quickstart/).
- [Kafka 4.1: design / delivery semantics](https://kafka.apache.org/41/design/design/).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
