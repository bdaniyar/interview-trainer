# Explicit transactions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Explicit transactions**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``begin``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

An explicit transaction boundary groups all database changes of one use case into one commit/rollback decision.

### Как работает

`with session.begin()` commits on normal exit and rolls back on exception; repositories should not secretly finalize independent parts.


### Важный нюанс / limitation

Keep external network calls outside the transaction when possible to reduce lock/connection time.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `begin`
- atomic service operation
- avoid commits hidden across repository calls

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Explicit transactions: отдельный пример

```python
def transfer(session, source, target, amount):
    raise NotImplementedError
```

Это публичный starter contract практики «Explicit transfer transaction». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Multiple hidden repository commits make partial data durable when a later step fails.

## Practice

**A · Code/result prediction.** Change one input in the ``begin`` example and predict the result before running it.

**B · Find the bug.** Find code that violates `atomic service operation` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``begin`` and add one edge-case test.

**E · Interview explanation.** Explain Explicit transactions in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Explicit transactions и как это работает?

### Follow-up

Какая типичная ошибка связана с Explicit transactions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

An explicit transaction boundary groups all database changes of one use case into one commit/rollback decision.

### Нормальный Junior answer

> An explicit transaction boundary groups all database changes of one use case into one commit/rollback decision. `with session.begin()` commits on normal exit and rolls back on exception; repositories should not secretly finalize independent parts. Важное ограничение: Keep external network calls outside the transaction when possible to reduce lock/connection time.

### Углубление / follow-up

**Какая типичная ошибка связана с Explicit transactions?**

Multiple hidden repository commits make partial data durable when a later step fails.

## Expected answer rubric

### Must mention

- `begin`
- atomic service operation
- avoid commits hidden across repository calls

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Multiple hidden repository commits make partial data durable when a later step fails.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Explicit transactions?

## Задача

### Explicit transfer transaction

transfer проверяет positive amount/balance и меняет два Account внутри session.begin.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** An explicit transaction boundary groups all database changes of one use case into one commit/rollback decision.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Multiple hidden repository commits make partial data durable when a later step fails.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
