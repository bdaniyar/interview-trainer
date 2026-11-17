# Dependency injection

## Суть

Dependency Injection передаёт зависимость компоненту снаружи. BookingService получает способ записать событие, поэтому сам не решает, использовать локальный notification module или durable outbox.

## Учебные цели

Передать BookingService зависимость через constructor и собрать две реализации в composition root. Сравнить реальное поведение local adapter и outbox adapter, сохранив общий узкий контракт.

## Зачем это нужно backend-разработчику

В composition root передайте adapter, который намеренно бросает RuntimeError после record. Проверьте rollback. Затем верните LocalNotificationAdapter/OutboxAdapter и сравните expected consistency в `scripts/test_architecture_lab.sh -k rollback`.

## Теория

### Что это

Dependency Injection передаёт зависимость компоненту снаружи. BookingService получает способ записать событие, поэтому сам не решает, использовать локальный notification module или durable outbox.

### Как работает

Конструктор принимает BookingEvents Protocol. Composition root в api.py создаёт LocalNotificationAdapter для MODE=monolith, иначе OutboxAdapter. Код use case вызывает record через один контракт. Для такого решения не нужен отдельный DI framework или глобальный container.

FastAPI Depends может создавать request dependencies, но не определяет автоматически правильную transaction boundary и lifetime DB session. Заводите ресурсы на понятное время, освобождайте их и не передавайте закрытую session в background callback.

Service Locator скрывает обращения к глобальному реестру внутри функции; constructor injection делает требования видимыми в signature. Fake adapter полезен для маленького unit test, но корректность SQL locks/rollback доказывают отдельные real DB tests.

### Важный нюанс / ограничение

DI упрощает замену dependency, но не делает её эффекты одинаковыми. Local adapter участвует в текущем COMMIT, outbox adapter оставляет внешнюю доставку на потом.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

DI — способ передачи зависимости, а не обязательный framework. Protocol описывает нужную операцию; composition root выбирает concrete implementation. Lifetime подключения и транзакции должен соответствовать одной операции, а не случайному глобальному singleton.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'rollback or two_requests'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Создать dependency внутри service — скрыть выбор реализации. Передавать целый service locator — сделать зависимости неявными. Подменить repository mock и считать доказанным PostgreSQL locking — проверить только взаимодействие объектов. Сохранить connection между запросами — смешать lifetime и ownership ресурса.

## Практика

В composition root передайте adapter, который намеренно бросает RuntimeError после record. Проверьте rollback. Затем верните LocalNotificationAdapter/OutboxAdapter и сравните expected consistency в `scripts/test_architecture_lab.sh -k rollback`.

## Вопросы с собеседований

1. Нужен ли container для Dependency Injection?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Нет. Передача зависимости в конструктор уже является DI. Container лишь автоматизирует сборку и lifetime, которые всё равно нужно определить.

DI упрощает замену dependency, но не делает её эффекты одинаковыми. Local adapter участвует в текущем COMMIT, outbox adapter оставляет внешнюю доставку на потом.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

В composition root передайте adapter, который намеренно бросает RuntimeError после record. Проверьте rollback. Затем верните LocalNotificationAdapter/OutboxAdapter и сравните expected consistency в `scripts/test_architecture_lab.sh -k rollback`.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Компонент получает то, что ему нужно; composition root решает, какую реализацию дать. Сигнатура задаёт форму вызова, документация и integration tests — его эффекты, ошибки и transaction boundary.

## Источники

- [Fowler 2004: Dependency Injection](https://martinfowler.com/articles/injection.html).
- [FastAPI: dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
