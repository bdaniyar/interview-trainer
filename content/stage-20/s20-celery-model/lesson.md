# Celery model

## Суть

Celery разделяет producer, broker и worker. Producer публикует имя зарегистрированной задачи и сериализованные аргументы. Worker получает сообщение и запускает код. Result backend — отдельный механизм хранения результата, а не само задание в broker.

## Учебные цели

Проследить путь зарегистрированной задачи от producer через Redis к настоящему Celery worker. Прочитать результат из отдельного backend и объяснить, на какой границе действует acknowledgement.

## Зачем это нужно backend-разработчику

Откройте `projects/durable_queue/queue_app/celery_demo.py`: подпишите producer, зарегистрированное имя, broker, result backend, ack и visibility timeout. Запустите broker test. В копии задачи верните неверную сумму: настоящий result assertion должен упасть. Не подключайте Celery к student Python Runner.

## Теория

### Что это

Celery разделяет producer, broker и worker. Producer публикует имя зарегистрированной задачи и сериализованные аргументы. Worker получает сообщение и запускает код. Result backend — отдельный механизм хранения результата, а не само задание в broker.

### Как работает

В нашем сравнении Redis DB0 хранит transport data, Redis DB1 — task results. Одинаковый Redis server не делает назначения одинаковыми. Worker заранее импортирует зарегистрированную task; передавать произвольный Python-код в сообщение не требуется. Используйте JSON и проверяйте payload.

Producer publish, broker acceptance, получение worker и успешный business COMMIT — разные события. task_acks_late переносит acknowledgement ближе к завершению, но само по себе не гарантирует повтор после любого child-process loss. В Celery 5.5.3 task_reject_on_worker_lost меняет это поведение и может создать poison-message loop; нужен ограниченный протокол ошибок и идемпотентные эффекты.

Concurrency и prefetch управляют числом исполняемых и заранее зарезервированных задач. worker_prefetch_multiplier=1 помогает равномернее раздавать долгие задания, но не превращает очередь в строгий глобальный FIFO завершений. Нельзя использовать result.state=PENDING как доказательство «worker ещё не начал»: результат также может отсутствовать или истечь.

### Важный нюанс / ограничение

Учебная Celery task — чистая сумма квадратов без внешнего эффекта. Основной durable проект реализован на PostgreSQL явно, чтобы видеть claim/lease/fencing. Celery comparison не доказывает надёжность произвольных side effects.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Producer и worker должны согласовать имя task и формат аргументов. Broker, result backend и business database выполняют разные роли. Concurrency ограничивает выполнение, prefetch — предварительно взятые сообщения; PENDING в result backend не является точным состоянием очереди.

## Примеры кода

```sh
docker compose -f projects/durable_queue/compose.brokers.yml run --rm client
```

В отдельном network запускается настоящий Celery worker с concurrency=1. Producer вызывает comparison.sum_squares(10), result.get получает Python int 385 из DB1. В итоговом JSON celery_real_worker_and_result=true появляется только после ответа worker; импорт декоратора не считается выполнением.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Запустить producer без worker и ждать вычисления — оставить сообщение без исполнителя. Считать импорт декоратора доказательством доставки — не проверить транспорт. Включить acks_late и забыть о worker-loss, повторных эффектах и poison messages — оставить важные failure paths без контракта.

## Практика

Откройте `projects/durable_queue/queue_app/celery_demo.py`: подпишите producer, зарегистрированное имя, broker, result backend, ack и visibility timeout. Запустите broker test. В копии задачи верните неверную сумму: настоящий result assertion должен упасть. Не подключайте Celery к student Python Runner.

## Вопросы с собеседований

1. Чем broker отличается от result backend?
2. Достаточно ли acks_late для exactly-once business effect?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Broker доставляет сообщения worker, result backend хранит состояние/результаты task; один не подменяет другой.

Нет. Повторная доставка возможна, некоторые worker-loss пути требуют отдельной настройки, а эффект должен быть идемпотентным по собственной границе.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

Откройте `projects/durable_queue/queue_app/celery_demo.py`: подпишите producer, зарегистрированное имя, broker, result backend, ack и visibility timeout. Запустите broker test. В копии задачи верните неверную сумму: настоящий result assertion должен упасть. Не подключайте Celery к student Python Runner.

Внесите изменение в свою копию проекта и запустите соответствующий integration test. Критерий успеха — сохранённый invariant и ожидаемый failure при намеренно сломанной границе; текстовое объяснение автоматически не оценивается.

## Шпаргалка

Task name + JSON идут в broker; worker исполняет зарегистрированный код; result backend хранит результат. Поздний ack меняет момент подтверждения, но идемпотентность эффекта остаётся ответственностью приложения. Тест ждёт реальное значение 385 от отдельного worker.

## Источники

- [Celery 5.5.3: First steps / architecture](https://docs.celeryq.dev/en/v5.5.3/getting-started/first-steps-with-celery.html).
- [Celery 5.5.3: Tasks / acks_late and worker lost](https://docs.celeryq.dev/en/v5.5.3/userguide/tasks.html).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
