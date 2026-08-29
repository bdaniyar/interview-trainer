# SQLAlchemy 2.x `select`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **SQLAlchemy 2.x `select`**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``select``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

SQLAlchemy 2.x `select()` builds an explicit SQL expression executed through Session.

### Как работает

`where` adds predicates; `session.scalars(statement)` returns the first selected entity/value column; `one_or_none` enforces at most one row while `first` merely takes one.


### Важный нюанс / limitation

Choose result method according to cardinality instead of silently ignoring duplicate rows.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `select`
- `where`
- result/scalars
- `.one_or_none`

### Полезно

- `.first`
- multiple rows

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### SQLAlchemy 2.x `select`: отдельный пример

```python
def active_users_statement(User):
    raise NotImplementedError
```

Это публичный starter contract практики «SQLAlchemy select». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Using `.first()` where uniqueness is required hides duplicate-data bugs that `.one_or_none()` would expose.

## Practice

**A · Code/result prediction.** Change one input in the ``select`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``where`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``select`` and add one edge-case test.

**E · Interview explanation.** Explain SQLAlchemy 2.x `select` in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое SQLAlchemy 2.x `select` и как это работает?

### Follow-up

Какая типичная ошибка связана с SQLAlchemy 2.x `select`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

SQLAlchemy 2.x `select()` builds an explicit SQL expression executed through Session.

### Нормальный Junior answer

> SQLAlchemy 2.x `select()` builds an explicit SQL expression executed through Session. `where` adds predicates; `session.scalars(statement)` returns the first selected entity/value column; `one_or_none` enforces at most one row while `first` merely takes one. Важное ограничение: Choose result method according to cardinality instead of silently ignoring duplicate rows.

### Углубление / follow-up

**Какая типичная ошибка связана с SQLAlchemy 2.x `select`?**

Using `.first()` where uniqueness is required hides duplicate-data bugs that `.one_or_none()` would expose.

## Expected answer rubric

### Must mention

- `select`
- `where`
- result/scalars
- `.one_or_none`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using `.first()` where uniqueness is required hides duplicate-data bugs that `.one_or_none()` would expose.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с SQLAlchemy 2.x `select`?

## Задача

### SQLAlchemy select

active_users_statement(User): select active true, order by id.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** SQLAlchemy 2.x `select()` builds an explicit SQL expression executed through Session.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Using `.first()` where uniqueness is required hides duplicate-data bugs that `.one_or_none()` would expose.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
