# Scaling sequence

## Суть

Масштабирование начинается с наблюдаемого bottleneck и нужного service contract. Добавить replicas полезно, когда нагрузка действительно распределяется и общий ресурс не становится следующим ограничением.

## Учебные цели

Предложить следующий шаг масштабирования по наблюдаемому bottleneck. Для каждого шага назвать метрику успеха, предел общего ресурса и invariant, который обязан сохраниться.

## Зачем это нужно backend-разработчику

Запустите `scripts/test_architecture_lab.sh -k stateless`, затем разберите backlog при недоступном receiver. Предложите три метрики: oldest-ready age, retry/failed count, DB pool wait. Не используйте UUID каждого события как metric label.

## Теория

### Что это

Масштабирование начинается с наблюдаемого bottleneck и нужного service contract. Добавить replicas полезно, когда нагрузка действительно распределяется и общий ресурс не становится следующим ограничением.

### Как работает

Для API сначала измерьте route latency/errors, CPU, DB query plans, locks и pool saturation. Stateless instances позволяют распределять запросы, но требуют общего concurrency budget. Для worker измеряйте backlog age, attempts, expired leases и processing latency; добавляйте процессы в пределах DB/downstream capacity.

Cache может снизить чтения, но не заменяет атомарный booking invariant. Реплика БД может отставать, поэтому read-after-write контракт и routing нужно определить явно. Service extraction даёт отдельный release/scale boundary ценой сети, retries и operational work.

В стенде два API process делят устойчивое состояние и idempotency contract. JSON logs содержат correlation_id и duration_ms, relay пишет delivery attempt. Это рабочий минимум диагностики, но не benchmark, trace collector, autoscaler или production alerting. Trace span tree и metrics требуют отдельной instrumentation и безопасной cardinality.

### Важный нюанс / ограничение

Нельзя обещать линейный рост capacity или точную latency без измерений. Выбирайте шаг по данным и проверяйте сохранность invariants после изменения.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Latency, throughput, error rate и saturation описывают разные стороны нагрузки. Медленный query, CPU-bound обработка и downstream rate limit требуют разных изменений. Queue сглаживает всплеск, но не увеличивает устойчивую скорость потребителя сама по себе.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'retry_budget or stateless'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Добавлять replicas к API при насыщенной БД — увеличить конкуренцию. Включить cache без политики stale read — изменить видимую корректность. Перейти к микросервисам ради неопределённой «масштабируемости» — добавить operational cost без доказанного bottleneck. Измерять только среднее время — пропустить длинный хвост и ошибки.

## Практика

Запустите `scripts/test_architecture_lab.sh -k stateless`, затем разберите backlog при недоступном receiver. Предложите три метрики: oldest-ready age, retry/failed count, DB pool wait. Не используйте UUID каждого события как metric label.

## Вопросы с собеседований

1. Когда добавление workers ухудшает систему?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Когда они перегружают общую БД, connection pool или downstream, усиливают retries и конкуренцию. Нужны измерения, concurrency limits и backpressure.

Нельзя обещать линейный рост capacity или точную latency без измерений. Выбирайте шаг по данным и проверяйте сохранность invariants после изменения.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Запустите `scripts/test_architecture_lab.sh -k stateless`, затем разберите backlog при недоступном receiver. Предложите три метрики: oldest-ready age, retry/failed count, DB pool wait. Не используйте UUID каждого события как metric label.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Измерьте нагрузку и предел → сформулируйте гипотезу → измените один существенный фактор → сравните метрики и correctness tests. Отдельно проверяйте connection budget, backlog и downstream limits. Число контейнеров не является доказательством capacity.

## Источники

- [OpenTelemetry: trace concepts](https://opentelemetry.io/docs/concepts/signals/traces/).
- [PostgreSQL 17: EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
