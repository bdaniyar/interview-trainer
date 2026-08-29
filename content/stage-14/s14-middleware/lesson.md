# Middleware

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Middleware**, а не только запомнить термин;
- прочитать и изменить короткий пример для `request/response wrapper`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Middleware wraps the request/response flow for cross-cutting behavior such as request IDs, timing or security headers.

### Как работает

Each middleware runs before the inner app and after it returns; order therefore changes observation and error behavior.


### Важный нюанс / limitation

Domain authorization usually needs resolved user/resource context and belongs in dependencies/services, not generic middleware.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- request/response wrapper
- timing/request ID
- ordering
- not for domain logic

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Middleware: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь middleware и endpoint.
```

Это публичный starter contract практики «Request-ID middleware». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Reading a streaming request body in middleware without replaying it can leave the endpoint with no body.

## Practice

**A · Code/result prediction.** Change one input in the `request/response wrapper` example and predict the result before running it.

**B · Find the bug.** Find code that violates `timing/request ID` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `request/response wrapper` and add one edge-case test.

**E · Interview explanation.** Explain Middleware in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Middleware и как это работает?

### Follow-up

Какая типичная ошибка связана с Middleware?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Middleware wraps the request/response flow for cross-cutting behavior such as request IDs, timing or security headers.

### Нормальный Junior answer

> Middleware wraps the request/response flow for cross-cutting behavior such as request IDs, timing or security headers. Each middleware runs before the inner app and after it returns; order therefore changes observation and error behavior. Важное ограничение: Domain authorization usually needs resolved user/resource context and belongs in dependencies/services, not generic middleware.

### Углубление / follow-up

**Какая типичная ошибка связана с Middleware?**

Reading a streaming request body in middleware without replaying it can leave the endpoint with no body.

## Expected answer rubric

### Must mention

- request/response wrapper
- timing/request ID
- ordering
- not for domain logic

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Reading a streaming request body in middleware without replaying it can leave the endpoint with no body.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Middleware?

## Задача

### Request-ID middleware

Response X-Request-ID равен входному header либо новому UUID; GET /ping возвращает pong.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Middleware wraps the request/response flow for cross-cutting behavior such as request IDs, timing or security headers.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Reading a streaming request body in middleware without replaying it can leave the endpoint with no body.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
