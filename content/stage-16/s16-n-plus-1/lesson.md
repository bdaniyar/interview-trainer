# N+1

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **N+1**, а не только запомнить термин;
- прочитать и изменить короткий пример для `one parent query plus per-row child query`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

N+1 is one query for parent rows followed by one relationship query per parent.

### Как работает

Lazy loading triggers the repeated queries; detect it in SQL logs or a query-count test and choose `selectinload`, `joinedload` or explicit projection based on cardinality.


### Важный нюанс / limitation

Eager-load only data the use case needs; a giant joined graph can create row multiplication and memory cost.

### Где используется в backend

Listing users with roles is a common N+1 path when serialization touches each lazy relationship.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- one parent query plus per-row child query
- detection
- logs/query count
- eager loading

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### N+1: отдельный пример

```text
Сценарий: Список 100 users выполняет ещё 100 SELECT roles.

Проверка:
Посчитать queries и использовать selectinload/joinedload по cardinality; integration test с query counter.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Adding a cache does not fix an ORM query shape that issues hundreds of avoidable round trips.

## Practice

**A · Code/result prediction.** Change one input in the `one parent query plus per-row child query` example and predict the result before running it.

**B · Find the bug.** Find code that violates `detection` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `one parent query plus per-row child query` and add one edge-case test.

**E · Interview explanation.** Explain N+1 in 45–60 seconds and include one limitation.

## Debugging practice

### N+1

**Сценарий:** Список 100 users выполняет ещё 100 SELECT roles.

**Rubric:** Посчитать queries и использовать selectinload/joinedload по cardinality; integration test с query counter.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое N+1 и как это работает?

### Follow-up

Какая типичная ошибка связана с N+1?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

N+1 is one query for parent rows followed by one relationship query per parent.

### Нормальный Junior answer

> N+1 is one query for parent rows followed by one relationship query per parent. Lazy loading triggers the repeated queries; detect it in SQL logs or a query-count test and choose `selectinload`, `joinedload` or explicit projection based on cardinality. Важное ограничение: Eager-load only data the use case needs; a giant joined graph can create row multiplication and memory cost.

### Углубление / follow-up

**Какая типичная ошибка связана с N+1?**

Adding a cache does not fix an ORM query shape that issues hundreds of avoidable round trips.

## Expected answer rubric

### Must mention

- one parent query plus per-row child query
- detection
- logs/query count
- eager loading

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Adding a cache does not fix an ORM query shape that issues hundreds of avoidable round trips.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с N+1?

## Задача

### Убрать N+1

users_with_roles(User): select + selectinload(User.roles), order id.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** N+1 is one query for parent rows followed by one relationship query per parent.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Adding a cache does not fix an ORM query shape that issues hundreds of avoidable round trips.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
