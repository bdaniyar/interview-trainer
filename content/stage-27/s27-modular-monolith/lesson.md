# Modular monolith

## Суть

Модульный монолит сохраняет один deployable, но разделяет бизнес-возможности явными API. Модуль бронирования не должен произвольно переписывать внутренние таблицы notification модуля.

## Учебные цели

Разделить booking и notification явным контрактом внутри одного deployable. Найти владельца каждой таблицы и проследить общую транзакцию через узкий adapter.

## Зачем это нужно backend-разработчику

В `architecture/orders.py` найдите BookingEvents, LocalNotificationAdapter и OutboxAdapter. Замените adapter в composition root и запустите rollback/stale-read tests. Подпишите, какой COMMIT теперь перестал включать notification.

## Теория

### Что это

Модульный монолит сохраняет один deployable, но разделяет бизнес-возможности явными API. Модуль бронирования не должен произвольно переписывать внутренние таблицы notification модуля.

### Как работает

В примере orders отвечает за inventory/booking, notifications — за inbox/effect. BookingService обращается к узкому BookingEvents Protocol. LocalNotificationAdapter вызывает публичную функцию notification module с общей transaction. Такое разделение делает зависимость видимой и позволяет заменить способ записи intent.

Общая БД не заставляет все таблицы быть общедоступными по договорённости. Контракт модуля, import boundaries и review удерживают coupling. Одни папки не обеспечивают модульность: если endpoint знает schema каждого соседа, изменение одной сущности разносится по приложению.

Выделение service меняет контракт отказов. Вызов функции, который мог участвовать в общем COMMIT, превращается в remote operation. Наш OutboxAdapter фиксирует intent локально, relay позже доставляет его в другой сервис. Это изменение consistency, а не только новый Dockerfile.

### Важный нюанс / ограничение

Module boundary и transaction boundary связаны, но не обязаны совпадать. Общая локальная transaction допустима в monolith; после выделения service прежнюю атомарность нельзя подразумевать.

## Модель понимания

Проследите один booking от HTTP до durable state. Подпишите владельца данных и каждый COMMIT. На сетевой границе отдельно отметьте timeout, возможный повтор и наблюдаемое состояние receiver.

## Что нужно знать на Junior

### Обязательно

Модуль публикует операции, а не разрешение менять любые внутренние таблицы. Composition root собирает зависимости. Изменение одного модуля должно требовать согласования его контракта, а не знания всех деталей его хранения.

## Примеры кода

Из корня репозитория запустите конкретный исполняемый пример на настоящих PostgreSQL и HTTP:

```sh
scripts/test_architecture_lab.sh -k 'rollback or stale'
```

Полный workflow, endpoints и сравнение двух вариантов описаны в `projects/architecture_lab/README.md`. Test project использует собственный tmpfs и не читает SQLite Pythoria. Ожидаемые состояния заданы ниже и в соответствующем pytest; число реально запущенных tests отображается в выводе.

## Типичные ошибки

Разложить файлы по папкам, но оставить произвольные обращения к чужим таблицам — сохранить сильное сцепление. Скрыть COMMIT внутри каждого метода — разрушить общую бизнес-операцию. При выносе модуля в HTTP-сервис забыть изменить контракт атомарности — получить частичный результат.

## Практика

В `architecture/orders.py` найдите BookingEvents, LocalNotificationAdapter и OutboxAdapter. Замените adapter в composition root и запустите rollback/stale-read tests. Подпишите, какой COMMIT теперь перестал включать notification.

## Вопросы с собеседований

1. Почему много папок ещё не modular monolith?
2. Какой предел гарантии важно назвать в этой теме?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Нужны границы ответственности и публичные module contracts. Прямые обращения к внутренностям соседей сохраняют сильную связанность независимо от структуры папок.

Module boundary и transaction boundary связаны, но не обязаны совпадать. Общая локальная transaction допустима в monolith; после выделения service прежнюю атомарность нельзя подразумевать.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Назовите владельца данных, transaction boundary, поведение при partial failure и способ восстановления. Покажите конкретное доказательство в project test. Отличайте локальную атомарность, durable intent, доставку и внешний эффект.

</details>

## Задача

В `architecture/orders.py` найдите BookingEvents, LocalNotificationAdapter и OutboxAdapter. Замените adapter в composition root и запустите rollback/stale-read tests. Подпишите, какой COMMIT теперь перестал включать notification.

Сохраните working code своей копии и объяснение двух transaction boundaries. Соответствующий test должен проходить на корректном варианте и обнаруживать намеренно внесённую ошибку. Это локальный project exercise; обычный Python Runner не получает Docker/сеть, а текстовый ответ автоматически не оценивается.

## Шпаргалка

Один release, несколько ответственных модулей, узкие явные API. Общий COMMIT задаётся use case. Подготовка к выделению сервиса начинается с ownership и контракта, а переход к сети требует нового протокола согласованности.

## Источники

- [Cockburn: Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture).
- [Fowler: Microservices / componentization](https://martinfowler.com/articles/microservices.html).

Секции первоисточников сверены 2026-11-16. Практика: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; точные pins и ограничения находятся в project README. Название architecture pattern не выдаётся за измерение performance или production readiness.
