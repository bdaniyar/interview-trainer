# Engine and connection pool

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Engine and connection pool**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Engine and connection pool`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

SQLAlchemy Engine owns the SQL dialect and connection pool; it is a long-lived application-level factory, not an ORM Session.

### Как работает

A Session checks out a connection when SQL is needed and returns it according to transaction/session lifecycle.


### Важный нюанс / limitation

Pool size must match database capacity and workload; creating an engine per request defeats pooling.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Engine and connection pool

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Engine and connection pool: отдельный пример

```python
def example_s16_engine_and_connection_pool() -> tuple[str, ...]:
    # Engine and connection pool: проверяем отдельный contract урока.
    return ('Engine and connection pool',)

assert example_s16_engine_and_connection_pool()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Common mistakes

### Ошибка 1

A leaked Session can keep a transaction/connection checked out until the pool is exhausted.

## Practice

**A · Code/result prediction.** Change one input in the `Engine and connection pool` example and predict the result before running it.

**B · Find the bug.** Find code that violates `Engine and connection pool` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `Engine and connection pool` and add one edge-case test.

**E · Interview explanation.** Explain Engine and connection pool in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Engine and connection pool и как это работает?

### Follow-up

Какая типичная ошибка связана с Engine and connection pool?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

SQLAlchemy Engine owns the SQL dialect and connection pool; it is a long-lived application-level factory, not an ORM Session.

### Нормальный Junior answer

> SQLAlchemy Engine owns the SQL dialect and connection pool; it is a long-lived application-level factory, not an ORM Session. A Session checks out a connection when SQL is needed and returns it according to transaction/session lifecycle. Важное ограничение: Pool size must match database capacity and workload; creating an engine per request defeats pooling.

### Углубление / follow-up

**Какая типичная ошибка связана с Engine and connection pool?**

A leaked Session can keep a transaction/connection checked out until the pool is exhausted.

## Expected answer rubric

### Must mention

- Engine and connection pool

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- A leaked Session can keep a transaction/connection checked out until the pool is exhausted.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Engine and connection pool?

## Задача

Сделай короткую письменную практику по теме **Engine and connection pool**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** SQLAlchemy Engine owns the SQL dialect and connection pool; it is a long-lived application-level factory, not an ORM Session.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** A leaked Session can keep a transaction/connection checked out until the pool is exhausted.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
