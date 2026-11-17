# Delivery semantics

## Суть

Сообщение и бизнес-эффект — разные объекты. Надёжность требует описать, кто имеет право выполнять работу, что происходит после падения и как повтор влияет на результат. Здесь собран отдельный advanced worker protocol: atomic claim, lease, heartbeat и fencing.

## Учебные цели

Научиться отличать доставку сообщения от выполнения и фиксации эффекта. Проследить смену владельца job после падения, объяснить роль generation и проверить гонку отмены с завершением.

## Зачем это нужно backend-разработчику

Представьте обработку отчёта: worker A завис, worker B подхватил задание, затем A вернулся с результатом. Без защиты устаревший A может перезаписать состояние, уже изменённое B или отменой пользователя. Поэтому право записывать результат должно проверяться самим хранилищем в момент изменения.

## Теория

### Что это

At-most-once допускает потерю работы ради отсутствия повторной доставки. At-least-once допускает повторы ради восстановления после сбоя. Ни acknowledgement, ни количество запусков само по себе не определяет число бизнес-эффектов: это зависит от транзакции, уникального ключа и защиты конкретного ресурса.

### Как работает

SELECT FOR UPDATE SKIP LOCKED выбирает доступную строку, а UPDATE в той же транзакции устанавливает running, worker_id, lease_until, увеличивает attempts и generation. Два соединения не claim-ят одну доступную версию одновременно. После COMMIT row lock отпускается; вычисление идёт без долгой транзакции.

Lease — ограниченное временем право владения. Heartbeat продлевает его только для live текущего owner. Если worker завис и lease истёк, другой процесс claim-ит job с новой generation. Старый worker может вернуться: его локальная уверенность больше не имеет силы. Каждый finish/fail проверяет state, worker, точную generation и DB clock в одном UPDATE.

Fencing защищает конкретный guarded ресурс. Если старый worker уже отправил HTTP в незащищённый сервис, predicate в нашей БД не отменит внешний эффект. Нужен receiver idempotency key/fencing contract или явная обработка неизвестного исхода. Cancellation увеличивает generation; cancel и finish сериализуются row lock и дают один terminal winner.

SIGTERM прекращает новые claim и позволяет закончить текущую работу. SIGKILL не даёт выполнить finally: восстановление опирается на lease, durable state и ограниченный attempts. Количество процессов и размер DB pool ограничивают concurrency. Lease не является гарантией, что физически работает только один CPU-процесс: гарантируется, кто может COMMIT защищённый эффект.



### Отдельный advanced worker protocol

| Переход | Атомарное условие в БД | Что сохраняется |
| --- | --- | --- |
| queued → running | Задание готово, attempts < max, строка взята через SKIP LOCKED | Новая попытка, generation+1, владелец и срок lease |
| running → running / heartbeat | текущие owner+generation, lease ещё жив | новый lease_until |
| expired running → running / reclaim | старый lease истёк, budget остался | другая эпоха generation |
| running → succeeded | live ownership в том же UPDATE | result и unique effect в одной transaction |
| running → queued / retry | live owner, recoverable error, budget | available_at и освобождение ownership |
| queued/running → cancelled | строка ещё не terminal | generation+1, lease/owner очищены |

Heartbeat, который пришёл после срока lease, не получает право вернуть старое
владение. Если heartbeat и finish конкурируют с reclaim/cancel, решение принимает
порядок PostgreSQL row locks и guarded UPDATE, а не Python-проверка до запроса.
Старый worker может физически продолжать вычисление; запрещён именно его COMMIT
в защищённый ресурс. В другом сервисе такой guard нужно реализовать отдельно.

Polling пустой очереди содержит паузу; число worker processes ограничивает inflight
вычисления, а connection pool — только SQL connections. Транзакцию claim нельзя
держать всё время работы. На SIGTERM worker перестаёт claim-ить, завершает текущую
работу и heartbeat; на SIGKILL finally не выполняется, поэтому recovery опирается
на истечение lease и durable attempts. Сравните эти гарантии с actual crash tests.

### Важный нюанс / ограничение

At-least-once execution допускает несколько вычислений, но один защищённый локальный effect. Exactly-once нужно всегда уточнять по границе: наша транзакция не охватывает arbitrary external service.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Нужно уметь нарисовать claim → COMMIT → вычисление → guarded finish и указать место возможного падения. Знать, почему heartbeat не заменяет fencing, почему время берётся из БД и почему отмена должна конкурировать с завершением в одной системе блокировок.

## Примеры кода

```sh
scripts/test_durable_queue.sh
```

Тесты действительно завершают worker process после claim и во время управляемой работы. Новый owner получает большую generation; старый finish вызывает LostLease; effects содержит одну строку. Heartbeat test наблюдает продление lease в БД, а не просто считает вызовы mock.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Проверка generation отдельным SELECT оставляет окно гонки до UPDATE. Продление уже истёкшего lease может вернуть права старому worker после reclaim. Запись effect до проверки ownership оставляет дубль даже при правильном конечном состоянии job. Для каждой ошибки сравните durable state в stale-worker test; один только успешный ответ метода ничего не доказывает.

## Практика

Для job generation=7, state=running, lease_until=100 разберите worker_generation=6/7/8 и now=99/100/101. Затем решите модель can_commit ниже. После неё запустите реальные stale-worker, cancellation-race и crash tests проекта: Python boolean-модель сама по себе не доказывает atomic DB guard.

## Вопросы с собеседований

1. Почему одного lease_until недостаточно для stale protection?
2. Может ли lease предотвратить любой внешний дубль?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

После истечения lease появляется новый owner; старый процесс может вернуться. Generation и guarded UPDATE отличают эпохи владения и отклоняют stale finish.

Нет. Он защищает только ресурсы, проверяющие ownership/fencing. Внешний сервис должен поддерживать свой idempotency/fencing contract.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

Реализуйте `can_commit(state, current_generation, worker_generation, lease_until, now) -> bool` в main.py через обычные Python Run/Check. Верните True только для state="running", равных generation и now < lease_until. state — queued/running/succeeded/failed/cancelled. Generation — неотрицательные int без bool. Время — конечные int/float без bool. Неверные аргументы дают ValueError. Это модель проверки; в реальном worker условие проверяется атомарно базой по её часам.

Например, используйте входы из практики выше; граничные и неверные входы также проверяются. Starter намеренно не содержит готового алгоритма.

## Шпаргалка

Claim выдаёт новую эпоху владения. Heartbeat продлевает только ещё живую эпоху. Finish объединяет проверку прав, terminal transition и локальный effect. После потери lease процесс может работать физически, но не вправе фиксировать защищённый результат. Внешний receiver требует отдельного контракта дедупликации.

## Источники

- [PostgreSQL 17: SELECT locking / SKIP LOCKED](https://www.postgresql.org/docs/17/sql-select.html#SQL-FOR-UPDATE-SHARE).
- [PostgreSQL 17: explicit locking / row locks](https://www.postgresql.org/docs/17/explicit-locking.html).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
