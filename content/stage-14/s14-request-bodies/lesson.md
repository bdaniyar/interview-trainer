# Request bodies

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Request bodies**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Pydantic model`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A request body carries structured input; FastAPI commonly validates JSON through a Pydantic model.

### Как работает

Body bytes are decoded by media type, parsed as JSON and validated recursively before the endpoint receives a typed model.


### Важный нюанс / limitation

Schema validation handles shape/ranges; database-dependent business invariants belong in service logic/constraints.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Pydantic model
- JSON
- nested models
- validation

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Request bodies: отдельный пример

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Добавь model и endpoint.
```

Это публичный starter contract практики «Validated request body». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Using a raw dict everywhere loses generated schema, typed access and precise field errors.

## Practice

**A · Code/result prediction.** Change one input in the `Pydantic model` example and predict the result before running it.

**B · Find the bug.** Find code that violates `JSON` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `Pydantic model` and add one edge-case test.

**E · Interview explanation.** Explain Request bodies in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Request bodies и как это работает?

### Follow-up

Какая типичная ошибка связана с Request bodies?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A request body carries structured input; FastAPI commonly validates JSON through a Pydantic model.

### Нормальный Junior answer

> A request body carries structured input; FastAPI commonly validates JSON through a Pydantic model. Body bytes are decoded by media type, parsed as JSON and validated recursively before the endpoint receives a typed model. Важное ограничение: Schema validation handles shape/ranges; database-dependent business invariants belong in service logic/constraints.

### Углубление / follow-up

**Какая типичная ошибка связана с Request bodies?**

Using a raw dict everywhere loses generated schema, typed access and precise field errors.

## Expected answer rubric

### Must mention

- Pydantic model
- JSON
- nested models
- validation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using a raw dict everywhere loses generated schema, typed access and precise field errors.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Request bodies?

## Задача

### Validated request body

Создай BookingCreate(room_id > 0, guests 1..8) и POST /bookings → 201.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A request body carries structured input; FastAPI commonly validates JSON through a Pydantic model.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Using a raw dict everywhere loses generated schema, typed access and precise field errors.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
