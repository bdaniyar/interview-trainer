# Background jobs

## Суть

Фоновая работа отделяет принятие business operation от её дальнейшего исполнения. Архитектура должна назвать устойчивый intent, владельца работы, retry budget и наблюдаемое terminal state.

## Учебные цели

Включить job queue в архитектуру запроса, определить момент приёма и завершения и выбрать границу retry. Связать backlog, worker concurrency и ограничение downstream.

## Зачем это нужно backend-разработчику

Остановите relay, создайте booking с ключом `background-one`, убедитесь, что notification ещё нет. Запустите relay и проверьте доставку. Выполните producer-crash и timeout tests, затем объясните значение failed outbox после пяти ошибок.

## Теория

### Что это

Фоновая работа отделяет принятие business operation от её дальнейшего исполнения. Архитектура должна назвать устойчивый intent, владельца работы, retry budget и наблюдаемое terminal state.

### Как работает

Booking service COMMIT-ит booking+outbox. Relay независимо claim-ит event с SKIP LOCKED, lease и generation, отправляет HTTP вне transaction и guarded ack-ает успех. Падение процесса оставляет intent; истечение lease позволяет новому owner повторить тот же event_id.

Успешная доставка response не всегда наблюдаема producer: receiver мог COMMIT до timeout. Inbox на notification стороне дедуплицирует effect. Для произвольного внешнего сервиса без такого контракта остаётся неопределённый исход и reconciliation.

В job queue Stage 20 heartbeat продлевает вычислительный lease, attempts ограничивает retry, stale generation не может finish. В architecture relay короткий HTTP deadline меньше lease, пять deliveries затем failed; это отдельный простой протокол, а не бесконечный background callback.

### Важный нюанс / ограничение

Работа после response в памяти процесса не даёт durable recovery. Наличие worker требует ещё ownership, устойчивого state и ясной границы эффекта.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Job должна иметь durable identity, state, attempts и наблюдаемый результат. Worker владеет работой ограниченное время. Число процессов и inflight ограничивают нагрузку, а возраст ready queue показывает задержку, которую не видно по HTTP latency.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'producer or retry_budget'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Считать 202 завершённой работой — скрыть eventual state от клиента. Поставить job отдельно от business COMMIT — допустить потерянный intent. Не ограничивать retries и concurrency — усилить отказ downstream. Проверять лишь длину очереди — не заметить старую застрявшую работу.

## Практика

Остановите relay, создайте booking с ключом `background-one`, убедитесь, что notification ещё нет. Запустите relay и проверьте доставку. Выполните producer-crash и timeout tests, затем объясните значение failed outbox после пяти ошибок.

## Вопросы с собеседований

1. Что должно пережить падение worker?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Intent, attempt budget, идентичность операции и состояние ownership. Новый процесс должен восстановить работу, а старый не иметь права COMMIT stale effect.

Работа после response в памяти процесса не даёт durable recovery. Наличие worker требует ещё ownership, устойчивого state и ясной границы эффекта.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Остановите relay, создайте booking с ключом `background-one`, убедитесь, что notification ещё нет. Запустите relay и проверьте доставку. Выполните producer-crash и timeout tests, затем объясните значение failed outbox после пяти ошибок.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

API сохраняет intent, worker claim-ит, продлевает ownership и фиксирует effect. Повтор имеет бюджет и прежний business key. Наблюдайте ready age, running/expired, failed и downstream latency. Быстрый HTTP не означает быструю обработку.

## Источники

- [PostgreSQL 17: locking/SKIP LOCKED](https://www.postgresql.org/docs/17/sql-select.html#SQL-FOR-UPDATE-SHARE).
- [Celery 5.5.3: task reliability](https://docs.celeryq.dev/en/v5.5.3/userguide/tasks.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
