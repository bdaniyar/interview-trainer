# Path parameters

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Path parameters**, а не только запомнить термин;
- прочитать и изменить короткий пример для `type conversion`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A path parameter identifies part of the routed resource path and is converted/validated from text using the endpoint annotation.

### Как работает

`/users/{user_id}` binds the segment; constraints can reject invalid values before handler execution. Static routes must not be accidentally shadowed by a broad dynamic route.


### Важный нюанс / limitation

Path parameters are required by the matched path; optional filters belong in query parameters.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- type conversion
- validation
- routing order pitfalls

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Path parameters: отдельный пример

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/articles/{article_id}")
def article(article_id: int = Path(gt=0)):
    return {"article_id": article_id}
```

Router сначала сопоставляет path, затем FastAPI преобразует segment в `int` и применяет constraint `gt=0`.

## Common mistakes

### Ошибка 1

Registering `/users/{user_id}` before a conflicting `/users/me` design can route `me` into integer validation instead of the intended handler.

## Practice

**A · Code/result prediction.** Change one input in the `type conversion` example and predict the result before running it.

**B · Find the bug.** Find code that violates `validation` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `type conversion` and add one edge-case test.

**E · Interview explanation.** Explain Path parameters in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Path parameters и как это работает?

### Follow-up

Какая типичная ошибка связана с Path parameters?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A path parameter identifies part of the routed resource path and is converted/validated from text using the endpoint annotation.

### Нормальный Junior answer

> A path parameter identifies part of the routed resource path and is converted/validated from text using the endpoint annotation. `/users/{user_id}` binds the segment; constraints can reject invalid values before handler execution. Static routes must not be accidentally shadowed by a broad dynamic route. Важное ограничение: Path parameters are required by the matched path; optional filters belong in query parameters.

### Углубление / follow-up

**Какая типичная ошибка связана с Path parameters?**

Registering `/users/{user_id}` before a conflicting `/users/me` design can route `me` into integer validation instead of the intended handler.

## Expected answer rubric

### Must mention

- type conversion
- validation
- routing order pitfalls

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Registering `/users/{user_id}` before a conflicting `/users/me` design can route `me` into integer validation instead of the intended handler.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Path parameters?

## Задача

### Validated path parameter

GET /users/{user_id}: user_id >= 1; valid response содержит user_id, invalid даёт 422.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A path parameter identifies part of the routed resource path and is converted/validated from text using the endpoint annotation.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Registering `/users/{user_id}` before a conflicting `/users/me` design can route `me` into integer validation instead of the intended handler.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
