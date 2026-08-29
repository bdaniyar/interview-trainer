# Session lifecycle

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Session lifecycle**, а не только запомнить термин;
- прочитать и изменить короткий пример для `create`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Session lifecycle is create → use within one unit of work → commit or rollback → close.

### Как работает

A FastAPI yield-dependency can own one Session per request; service code decides the transaction outcome and cleanup always closes it.


### Важный нюанс / limitation

One AsyncSession must not be used concurrently by multiple tasks because it carries mutable transaction/identity state.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- create
- use
- commit/rollback
- close

### Полезно

- request-scoped session
- never share one session globally

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Session lifecycle: отдельный пример

```python
def example_s16_session_lifecycle() -> tuple[str, ...]:
    # Session lifecycle: проверяем отдельный contract урока.
    return ('create', 'use', 'commit/rollback', 'close',)

assert example_s16_session_lifecycle()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Common mistakes

### Ошибка 1

A module-global Session leaks tracked objects and transaction failures across requests.

## Practice

**A · Code/result prediction.** Change one input in the `create` example and predict the result before running it.

**B · Find the bug.** Find code that violates `use` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `create` and add one edge-case test.

**E · Interview explanation.** Explain Session lifecycle in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Session lifecycle и как это работает?

### Follow-up

Какая типичная ошибка связана с Session lifecycle?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Session lifecycle is create → use within one unit of work → commit or rollback → close.

### Нормальный Junior answer

> Session lifecycle is create → use within one unit of work → commit or rollback → close. A FastAPI yield-dependency can own one Session per request; service code decides the transaction outcome and cleanup always closes it. Важное ограничение: One AsyncSession must not be used concurrently by multiple tasks because it carries mutable transaction/identity state.

### Углубление / follow-up

**Какая типичная ошибка связана с Session lifecycle?**

A module-global Session leaks tracked objects and transaction failures across requests.

## Expected answer rubric

### Must mention

- create
- use
- commit/rollback
- close

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- A module-global Session leaks tracked objects and transaction failures across requests.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Session lifecycle?

## Задача

Сделай короткую письменную практику по теме **Session lifecycle**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Session lifecycle is create → use within one unit of work → commit or rollback → close.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** A module-global Session leaks tracked objects and transaction failures across requests.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
