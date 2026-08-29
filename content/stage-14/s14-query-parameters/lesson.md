# Query parameters

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Query parameters**, а не только запомнить термин;
- прочитать и изменить короткий пример для `optional/required`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Query parameters describe optional or required modifiers such as pagination, filtering and sorting after `?`.

### Как работает

FastAPI reads annotations/defaults and applies `Query` constraints; the resulting contract appears in OpenAPI.


### Важный нюанс / limitation

Set maximum page sizes and allowlist sort fields rather than interpolating arbitrary user input into SQL.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- optional/required
- aliases
- constraints
- pagination

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Query parameters: отдельный пример

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/articles")
def articles(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)):
    return {"limit": limit, "offset": offset}
```

Query parameters имеют независимые defaults и boundary constraints; pagination contract виден в OpenAPI.

## Common mistakes

### Ошибка 1

Treating `limit: int | None` as optional without a default still leaves it required.

## Practice

**A · Code/result prediction.** Change one input in the `optional/required` example and predict the result before running it.

**B · Find the bug.** Find code that violates `aliases` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `optional/required` and add one edge-case test.

**E · Interview explanation.** Explain Query parameters in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Query parameters и как это работает?

### Follow-up

Какая типичная ошибка связана с Query parameters?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Query parameters describe optional or required modifiers such as pagination, filtering and sorting after `?`.

### Нормальный Junior answer

> Query parameters describe optional or required modifiers such as pagination, filtering and sorting after `?`. FastAPI reads annotations/defaults and applies `Query` constraints; the resulting contract appears in OpenAPI. Важное ограничение: Set maximum page sizes and allowlist sort fields rather than interpolating arbitrary user input into SQL.

### Углубление / follow-up

**Какая типичная ошибка связана с Query parameters?**

Treating `limit: int | None` as optional without a default still leaves it required.

## Expected answer rubric

### Must mention

- optional/required
- aliases
- constraints
- pagination

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Treating `limit: int | None` as optional without a default still leaves it required.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Query parameters?

## Задача

### Pagination query

GET /items: offset >= 0, limit 1..100; defaults 0/20; верни оба значения.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Query parameters describe optional or required modifiers such as pagination, filtering and sorting after `?`.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Treating `limit: int | None` as optional without a default still leaves it required.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
