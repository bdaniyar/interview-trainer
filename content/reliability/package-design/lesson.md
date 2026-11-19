# Separation of concerns

## Суть

Separation of concerns отделяет HTTP-формат, бизнес-правило и хранение данных. Это помогает менять транспорт, не переписывая правило «последнее место нельзя продать дважды».

## Учебные цели

Найти отдельные причины изменения: HTTP-контракт, бизнес-правило и способ хранения. Проследить их зависимости и внести изменение, не перенося правило последнего места в транспортный слой.

## Зачем это нужно backend-разработчику

Найдите в `architecture/api.py` валидацию, в orders.py — reserve rule и в notifications.py — inbox. Добавьте неизвестный room_id=999 в HTTP test: ожидается 409 и отсутствие booking/outbox. Не переносите SQL в endpoint.

## Теория

### Что это

Separation of concerns отделяет HTTP-формат, бизнес-правило и хранение данных. Это помогает менять транспорт, не переписывая правило «последнее место нельзя продать дважды».

### Как работает

API layer проверяет room_id и Idempotency-Key, формирует status и correlation header. Application service задаёт use case и transaction boundary. Repository выполняет parameterized SQL. Notification module отвечает за дедупликацию собственного эффекта.

Нельзя считать любой код в service.py бизнес-логикой: если он лишь пересылает аргументы и размазывает COMMIT по wrappers, важная граница остаётся неявной. В проекте BookingService.place объединяет reserve и intent в engine.begin.

Ошибки тоже принадлежат своим уровням. SoldOut — ожидаемый бизнес-конфликт, HTTP adapter переводит его в 409. Потеря DB connection — инфраструктурная 503, после которой client повторяет с тем же ключом. Не возвращайте SQL traceback как domain response.

### Важный нюанс / ограничение

Разделение не требует новой прослойки для каждой строки. Проверяйте, упростилось ли изменение конкретного правила и стала ли transaction boundary яснее.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Файл или класс полезно выделять вокруг связной ответственности. Общий DTO может связать компоненты сильнее, чем кажется. Проверяйте область изменения конкретным сценарием: новый transport, новое правило или новая схема хранения.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'unknown or rollback'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Сделать общий utils модулем для всех несвязанных операций — скрыть ответственность. Дублировать правило бронирования в API и worker — получить разные результаты. Разбить код на множество тонких wrappers без собственного контракта — увеличить стоимость чтения без облегчения изменений.

## Практика

Найдите в `architecture/api.py` валидацию, в orders.py — reserve rule и в notifications.py — inbox. Добавьте неизвестный room_id=999 в HTTP test: ожидается 409 и отсутствие booking/outbox. Не переносите SQL в endpoint.

## Вопросы с собеседований

1. Где должна находиться граница транзакции use case?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Там, где определяется весь атомарный use case, обычно application service/unit of work. Отдельный COMMIT в каждом repository method разрушает общую атомарность.

Разделение не требует новой прослойки для каждой строки. Проверяйте, упростилось ли изменение конкретного правила и стала ли transaction boundary яснее.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Найдите в `architecture/api.py` валидацию, в orders.py — reserve rule и в notifications.py — inbox. Добавьте неизвестный room_id=999 в HTTP test: ожидается 409 и отсутствие booking/outbox. Не переносите SQL в endpoint.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Группируйте код по связным причинам изменения. Делайте зависимости явными. Правило хранится в одном месте; transport переводит вход и выход, persistence реализует операции. Число файлов не является мерой качества границ.

## Источники

- [Fowler: separating configuration from use](https://martinfowler.com/articles/injection.html).
- [SQLAlchemy 2.0: transaction scopes](https://docs.sqlalchemy.org/en/20/core/connections.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
