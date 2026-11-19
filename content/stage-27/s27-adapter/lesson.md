# Adapter

## Суть

Adapter переводит внешний механизм в контракт, который нужен приложению. BookingEvents.record выражает «сохранить intent события», а реализации выбирают local module или outbox.

## Учебные цели

Отделить нужный приложению контракт от деталей local notification и durable outbox. Проследить, какие данные и ошибки переводит adapter, и проверить обещание метода record на обеих реализациях.

## Зачем это нужно backend-разработчику

Добавьте adapter в своей копии и сохраните rollback contract `record` при исключении. Для HTTP варианта запустите `scripts/test_architecture_lab.sh -k timeout`; покажите, какой компонент хранит stable event_id и где находится receiver dedup.

## Теория

### Что это

Adapter переводит внешний механизм в контракт, который нужен приложению. BookingEvents.record выражает «сохранить intent события», а реализации выбирают local module или outbox.

### Как работает

LocalNotificationAdapter вызывает notification module с тем же connection. OutboxAdapter сериализует event и добавляет строку outbox в локальную DB. Отдельный relay — HTTP integration adapter: он отправляет JSON, задаёт deadline и сохраняет тот же event_id при retry.

Хороший adapter не прячет отличие гарантий. record для outbox означает устойчивый intent, а не доставленный email. Ответ receiver после timeout может потеряться, поэтому нельзя просто повторять с новым ID. Ошибки внешнего протокола переводятся в понятный application outcome, но неизвестный исход остаётся неизвестным.

Ports and Adapters не означает, что всё должно иметь interface. Начните с реально изменяемой границы и конкретного use case. В этом проекте connection всё ещё виден application service, что честно ограничивает независимость примера.

### Важный нюанс / ограничение

Одинаковый interface не делает local COMMIT и remote side effect эквивалентными. Название метода и документация должны описывать intent, а tests — фактическую boundary.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Adapter переводит один интерфейс в другой; DI выбирает и передаёт конкретную реализацию. Нужны ясные правила ошибок и ownership ресурсов. Метод record в проекте сохраняет intent; он не обещает уже отправленное внешнее уведомление.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'timeout or conflicting'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Переименовать HTTP-вызов в save и скрыть timeout — сделать контракт обманчивым. Проглотить ошибку adapter и вернуть успешный booking без сохранённого intent — потерять обязательную работу. Возвращать внешние SDK-типы через узкую границу — оставить зависимость от поставщика в use case.

## Практика

Добавьте adapter в своей копии и сохраните rollback contract `record` при исключении. Для HTTP варианта запустите `scripts/test_architecture_lab.sh -k timeout`; покажите, какой компонент хранит stable event_id и где находится receiver dedup.

## Вопросы с собеседований

1. Что adapter не должен скрывать от application contract?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Transaction boundary, возможный timeout/unknown outcome и смысл успеха. Нельзя выдавать запись outbox за завершённый внешний business effect.

Одинаковый interface не делает local COMMIT и remote side effect эквивалентными. Название метода и документация должны описывать intent, а tests — фактическую boundary.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

Добавьте adapter в своей копии и сохраните rollback contract `record` при исключении. Для HTTP варианта запустите `scripts/test_architecture_lab.sh -k timeout`; покажите, какой компонент хранит stable event_id и где находится receiver dedup.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Adapter переводит механизм в нужный контракт. Проверяйте форму данных, исключения, lifetime и реальные эффекты. Одинаковая сигнатура допустима лишь при согласованном обещании вызывающему коду; local и remote atomicity остаются разными.

## Источники

- [Cockburn 2005: Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture).
- [SQLAlchemy 2.0: transactions](https://docs.sqlalchemy.org/en/20/core/connections.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
