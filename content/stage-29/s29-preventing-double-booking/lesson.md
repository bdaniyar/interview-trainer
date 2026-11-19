# Preventing double booking

## Суть

Double booking появляется, когда два запроса принимают решение по одному старому состоянию. Оба могут увидеть available=1, поэтому чтение и последующая независимая запись не защищают последний ресурс.

## Учебные цели

Сформулировать invariant последней единицы и воспроизвести гонку независимыми соединениями. Проверить guarded decrement, атомарность booking/intent и корректный конфликт проигравшего запроса.

## Зачем это нужно backend-разработчику

Прочитайте Barrier в `test_actual_http_two_requests_do_not_double_book_and_replay_is_stable`. Измените свой вариант алгоритма на unsafe read/compute/write и сделайте barrier после двух чтений; воспроизведите нарушение. Верните atomic UPDATE и один invariant.

## Теория

### Что это

Double booking появляется, когда два запроса принимают решение по одному старому состоянию. Оба могут увидеть available=1, поэтому чтение и последующая независимая запись не защищают последний ресурс.

### Как работает

Условная запись UPDATE inventory SET available=available-1 WHERE id=:id AND available>0 RETURNING id объединяет проверку и изменение. Row lock сериализует конфликтующие записи. Отсутствие returned row означает, что резерв не получен; транзакция должна откатить связанные INSERT.

Альтернативы зависят от модели: SELECT FOR UPDATE с корректной общей transaction, SERIALIZABLE с retry всей transaction при 40001, unique/exclusion constraint для дискретного слота или интервала. Нельзя механически выбирать lock без определения invariant.

Deadlock и transient DB errors требуют ограниченного retry с тем же business key. Side effect вне БД не откатывается обычным ROLLBACK. Для оплаты после резерва нужны отдельный state machine и компенсации, а не долгий lock на всё время remote call.

### Важный нюанс / ограничение

Тест должен использовать независимые соединения и синхронизированный старт, а не два последовательных вызова или ненадёжную задержку.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Остаток не должен стать отрицательным; число успешных bookings не превышает исходный запас. Уникальный request key предотвращает повтор запроса, но два разных ключа всё равно конкурируют за один ресурс. Для интервалов нужны отдельная модель пересечения и подходящие constraints.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'two_requests and monolith'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Оба запроса читают available=1 и затем независимо пишут 0 — потерять изменение одного из них и продать два места. Защитить Python mutex только один процесс — оставить гонку между replicas. Проверять лишь два HTTP-status — пропустить лишнюю строку или потерянный остаток в БД.

## Практика

Прочитайте Barrier в `test_actual_http_two_requests_do_not_double_book_and_replay_is_stable`. Измените свой вариант алгоритма на unsafe read/compute/write и сделайте barrier после двух чтений; воспроизведите нарушение. Верните atomic UPDATE и один invariant.

## Вопросы с собеседований

1. Когда SERIALIZABLE требует повтор всей транзакции?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

При serialization failure 40001 решение на прежнем snapshot больше нельзя считать корректным. Нужно заново выполнить весь use case с ограниченным retry и тем же idempotency key.

Тест должен использовать независимые соединения и синхронизированный старт, а не два последовательных вызова или ненадёжную задержку.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Прочитайте Barrier в `test_actual_http_two_requests_do_not_double_book_and_replay_is_stable`. Измените свой вариант алгоритма на unsafe read/compute/write и сделайте barrier после двух чтений; воспроизведите нарушение. Верните atomic UPDATE и один invariant.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Guarded UPDATE или sound locking/constraint защищает ресурс в БД. Booking и intent фиксируются вместе. При одном месте два разных запроса дают одного победителя; повтор его ключа возвращает прежнюю бронь. После гонки проверяются строки и запас, а не только responses.

## Источники

- [PostgreSQL 17: row-level locks](https://www.postgresql.org/docs/17/explicit-locking.html).
- [PostgreSQL 17: serialization failures](https://www.postgresql.org/docs/17/mvcc-serialization-failure-handling.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
