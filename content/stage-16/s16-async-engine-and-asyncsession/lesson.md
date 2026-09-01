# Async engine and AsyncSession

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Async engine and AsyncSession**, а не только запомнить термин;
- прочитать и изменить короткий пример для `async driver`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

AsyncEngine и AsyncSession используют async DB driver, поэтому SQL I/O можно await без остановки event loop.

### Как работает

ORM state и transaction semantics сохраняются: одна AsyncSession на request или task, явный await для I/O и понятный владелец commit/rollback.


### Важный нюанс / ограничение

Не разделяй одну AsyncSession между tasks в `gather`: каждой concurrent единице нужна своя session и transaction.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- async driver
- awaitable operations
- one session per task/request
- не использовать одну AsyncSession конкурентно

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Async engine and AsyncSession: отдельный пример

```text
Сценарий: Две tasks используют одну AsyncSession.

Проверка:
Session per concurrent task/use case.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Переход на AsyncSession без async driver или с blocking data path не делает работу асинхронной.

## Практика

**A · Предсказание результата.** Измени один input в примере `async driver` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `awaitable operations`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `async driver`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Async engine and AsyncSession за 45–60 секунд и назови одно ограничение.

## Практика: Отладка

### Shared AsyncSession

**Сценарий:** Две tasks используют одну AsyncSession.

**Критерии ответа:** Session per concurrent task/use case.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Async engine and AsyncSession и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Async engine and AsyncSession?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

AsyncEngine и AsyncSession используют async DB driver, поэтому SQL I/O можно await без остановки event loop.

### Нормальный ответ уровня Junior

> AsyncEngine и AsyncSession используют async DB driver, поэтому SQL I/O можно await без остановки event loop. ORM state и transaction semantics сохраняются: одна AsyncSession на request или task, явный await для I/O и понятный владелец commit/rollback. Важное ограничение: Не разделяй одну AsyncSession между tasks в `gather`: каждой concurrent единице нужна своя session и transaction.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Async engine and AsyncSession?**

Переход на AsyncSession без async driver или с blocking data path не делает работу асинхронной.

## Критерии хорошего ответа

### Что обязательно упомянуть

- async driver
- awaitable operations
- one session per task/request
- не использовать одну AsyncSession конкурентно

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Переход на AsyncSession без async driver или с blocking data path не делает работу асинхронной.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Async engine and AsyncSession?

## Задача

Сделай короткую письменную практику по теме **Async engine and AsyncSession**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** AsyncEngine и AsyncSession используют async DB driver, поэтому SQL I/O можно await без остановки event loop.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Переход на AsyncSession без async driver или с blocking data path не делает работу асинхронной.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
