# Basic request path

## Суть

Путь backend-запроса проходит HTTP-вход, валидацию, use case, БД и ответ. Ошибка на каждом участке имеет разный смысл: неверный room_id, sold out и потеря DB connection не должны выглядеть одинаково.

## Учебные цели

Реализовать и проверить путь POST /bookings от валидации до COMMIT. Различить неверный вход, sold out, конфликт ключа и неизвестный результат после потери ответа.

## Зачем это нужно backend-разработчику

Отправьте room_id=1 с ключом `path-one` и correlation `path-trace`. Найдите HTTP log producer и receiver. Повторите key с тем же body, затем с room_id=2: ожидаются тот же UUID/200 и отдельный 409.

## Теория

### Что это

Путь backend-запроса проходит HTTP-вход, валидацию, use case, БД и ответ. Ошибка на каждом участке имеет разный смысл: неверный room_id, sold out и потеря DB connection не должны выглядеть одинаково.

### Как работает

POST /bookings принимает JSON room_id и Idempotency-Key. Pydantic отвергает неверную форму, service открывает transaction, PostgreSQL проверяет ограничения и резервирует место. После COMMIT response сообщает UUID. Клиент может потерять этот response и повторить тот же key.

Correlation ID проходит через HTTP middleware, outbox payload и notification receiver. Он помогает найти logs одного пути, но не служит ключом дедупликации. Idempotency-Key описывает business operation, event_id — отдельное событие.

HTTP timeout включает сетевое ожидание, а DB statement/lock timeout ограничивает другие участки. Не расходуйте на каждый внутренний retry полный новый бесконечный budget. Наблюдайте route latency/status и DB saturation; logs не должны содержать пароли или произвольный payload.

### Важный нюанс / ограничение

Успешный booking response подтверждает локальный COMMIT, а не уже доставленную notification. Потерянный response требует idempotent replay.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

HTTP validation проверяет форму входа; business constraint — допустимость операции. Binding parameters отделяет данные от SQL. Idempotency-Key связывает повтор с прежним результатом, а correlation ID помогает его найти в logs; это разные идентификаторы.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'actual_http'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Возвращать 200 на любую ошибку — скрыть, можно ли повторить операцию. Считать отсутствие HTTP-ответа rollback — допустить второй booking. Логировать весь payload и credentials — раскрыть ненужные данные. Проверять только happy path — не заметить конфликт ключа и гонку последнего места.

## Практика

Отправьте room_id=1 с ключом `path-one` и correlation `path-trace`. Найдите HTTP log producer и receiver. Повторите key с тем же body, затем с room_id=2: ожидаются тот же UUID/200 и отдельный 409.

## Вопросы с собеседований

1. Чем correlation ID отличается от idempotency key?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Первый связывает наблюдения по пути запроса, второй идентифицирует логическую бизнес-операцию для безопасного повтора. Их lifetime и область различаются.

Успешный booking response подтверждает локальный COMMIT, а не уже доставленную notification. Потерянный response требует idempotent replay.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Отправьте room_id=1 с ключом `path-one` и correlation `path-trace`. Найдите HTTP log producer и receiver. Повторите key с тем же body, затем с room_id=2: ожидаются тот же UUID/200 и отдельный 409.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Проверьте вход, сохраните invariant одной транзакцией, верните согласованный status. При неизвестном исходе повторите прежний operation key. Объясняйте отдельно durable booking и eventual notification; наблюдайте их по согласованным идентификаторам.

## Источники

- [FastAPI: request body](https://fastapi.tiangolo.com/tutorial/body/).
- [OpenTelemetry: trace concepts](https://opentelemetry.io/docs/concepts/signals/traces/).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
