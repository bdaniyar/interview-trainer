# Async engine and AsyncSession

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Async engine and AsyncSession**, а не только запомнить термин;
- прочитать и изменить короткий пример для `async driver`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

AsyncEngine and AsyncSession use an async DB driver so SQL I/O can be awaited without blocking the event loop.

### Как работает

ORM state/transaction semantics remain: one AsyncSession per request/task, explicit await for I/O and clear commit/rollback ownership.


### Важный нюанс / limitation

Do not share one AsyncSession across `gather` tasks; each concurrent unit needs its own session/transaction.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- async driver
- awaitable operations
- one session per task/request
- no concurrent use of one AsyncSession

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Async engine and AsyncSession: отдельный пример

```text
Сценарий: Две tasks используют одну AsyncSession.

Проверка:
Session per concurrent task/use case.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Switching to AsyncSession without an async driver or while using blocking migrations does not create an async data path.

## Practice

**A · Code/result prediction.** Change one input in the `async driver` example and predict the result before running it.

**B · Find the bug.** Find code that violates `awaitable operations` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `async driver` and add one edge-case test.

**E · Interview explanation.** Explain Async engine and AsyncSession in 45–60 seconds and include one limitation.

## Debugging practice

### Shared AsyncSession

**Сценарий:** Две tasks используют одну AsyncSession.

**Rubric:** Session per concurrent task/use case.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Async engine and AsyncSession и как это работает?

### Follow-up

Какая типичная ошибка связана с Async engine and AsyncSession?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

AsyncEngine and AsyncSession use an async DB driver so SQL I/O can be awaited without blocking the event loop.

### Нормальный Junior answer

> AsyncEngine and AsyncSession use an async DB driver so SQL I/O can be awaited without blocking the event loop. ORM state/transaction semantics remain: one AsyncSession per request/task, explicit await for I/O and clear commit/rollback ownership. Важное ограничение: Do not share one AsyncSession across `gather` tasks; each concurrent unit needs its own session/transaction.

### Углубление / follow-up

**Какая типичная ошибка связана с Async engine and AsyncSession?**

Switching to AsyncSession without an async driver or while using blocking migrations does not create an async data path.

## Expected answer rubric

### Must mention

- async driver
- awaitable operations
- one session per task/request
- no concurrent use of one AsyncSession

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Switching to AsyncSession without an async driver or while using blocking migrations does not create an async data path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Async engine and AsyncSession?

## Задача

Сделай короткую письменную практику по теме **Async engine and AsyncSession**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** AsyncEngine and AsyncSession use an async DB driver so SQL I/O can be awaited without blocking the event loop.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Switching to AsyncSession without an async driver or while using blocking migrations does not create an async data path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
