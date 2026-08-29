# Declarative models

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Declarative models**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``Mapped``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Declarative ORM models map Python classes/attributes to tables/columns using `Mapped` and `mapped_column` in SQLAlchemy 2.x.

### Как работает

Class metadata builds a SQL schema description used by ORM statements and migrations tooling; instances represent rows within Session state.


### Важный нюанс / limitation

Changing model code does not migrate an existing production database; Alembic revision must apply the schema transition.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `Mapped`
- `mapped_column`
- types
- primary keys

### Полезно

- constraints

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Declarative models: отдельный пример

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Создай User.
```

Это публичный starter contract практики «Declarative User model». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Calling `create_all` as a production migration strategy loses versioned, reviewable schema history.

## Practice

**A · Code/result prediction.** Change one input in the ``Mapped`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``mapped_column`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``Mapped`` and add one edge-case test.

**E · Interview explanation.** Explain Declarative models in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Declarative models и как это работает?

### Follow-up

Какая типичная ошибка связана с Declarative models?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Declarative ORM models map Python classes/attributes to tables/columns using `Mapped` and `mapped_column` in SQLAlchemy 2.x.

### Нормальный Junior answer

> Declarative ORM models map Python classes/attributes to tables/columns using `Mapped` and `mapped_column` in SQLAlchemy 2.x. Class metadata builds a SQL schema description used by ORM statements and migrations tooling; instances represent rows within Session state. Важное ограничение: Changing model code does not migrate an existing production database; Alembic revision must apply the schema transition.

### Углубление / follow-up

**Какая типичная ошибка связана с Declarative models?**

Calling `create_all` as a production migration strategy loses versioned, reviewable schema history.

## Expected answer rubric

### Must mention

- `Mapped`
- `mapped_column`
- types
- primary keys

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Calling `create_all` as a production migration strategy loses versioned, reviewable schema history.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Declarative models?

## Задача

### Declarative User model

SQLAlchemy 2.x User(id,email,active): email unique+index, active default True; Mapped/mapped_column.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Declarative ORM models map Python classes/attributes to tables/columns using `Mapped` and `mapped_column` in SQLAlchemy 2.x.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Calling `create_all` as a production migration strategy loses versioned, reviewable schema history.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
