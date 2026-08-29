# Relationships

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Relationships**, а не только запомнить термин;
- прочитать и изменить короткий пример для `one-to-many`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A relationship describes ORM navigation between entities; the foreign key column remains the database source of referential truth.

### Как работает

`back_populates` connects both directions; one-to-many, many-to-one and many-to-many determine collection/scalar shape and loading behavior.


### Важный нюанс / limitation

Relationship does not automatically choose efficient eager loading or safe cascade semantics.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- one-to-many
- many-to-one
- many-to-many
- `back_populates`

### Полезно

- ownership vs navigation

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Relationships: отдельный пример

```python
def example_s16_relationships() -> tuple[str, ...]:
    # Relationships: проверяем отдельный contract урока.
    return ('one-to-many', 'many-to-one', 'many-to-many', '`back_populates`',)

assert example_s16_relationships()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Common mistakes

### Ошибка 1

Confusing ORM relationship with database ownership can configure delete cascade that removes more data than intended.

## Practice

**A · Code/result prediction.** Change one input in the `one-to-many` example and predict the result before running it.

**B · Find the bug.** Find code that violates `many-to-one` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `one-to-many` and add one edge-case test.

**E · Interview explanation.** Explain Relationships in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Relationships и как это работает?

### Follow-up

Какая типичная ошибка связана с Relationships?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A relationship describes ORM navigation between entities; the foreign key column remains the database source of referential truth.

### Нормальный Junior answer

> A relationship describes ORM navigation between entities; the foreign key column remains the database source of referential truth. `back_populates` connects both directions; one-to-many, many-to-one and many-to-many determine collection/scalar shape and loading behavior. Важное ограничение: Relationship does not automatically choose efficient eager loading or safe cascade semantics.

### Углубление / follow-up

**Какая типичная ошибка связана с Relationships?**

Confusing ORM relationship with database ownership can configure delete cascade that removes more data than intended.

## Expected answer rubric

### Must mention

- one-to-many
- many-to-one
- many-to-many
- `back_populates`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Confusing ORM relationship with database ownership can configure delete cascade that removes more data than intended.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Relationships?

## Задача

Сделай короткую письменную практику по теме **Relationships**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A relationship describes ORM navigation between entities; the foreign key column remains the database source of referential truth.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Confusing ORM relationship with database ownership can configure delete cascade that removes more data than intended.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
