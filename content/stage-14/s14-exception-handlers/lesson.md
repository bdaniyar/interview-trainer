# Exception handlers

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Exception handlers**, а не только запомнить термин;
- прочитать и изменить короткий пример для `domain exception`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

An exception handler translates an exception type into a consistent HTTP response at an application/router boundary.

### Как работает

Domain code raises a meaningful domain exception; FastAPI handler maps it to status and safe payload while unexpected errors remain server failures.


### Важный нюанс / limitation

Do not catch every exception and convert programming bugs into 400 responses.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- domain exception
- HTTP mapping
- global handler
- avoid leaking internals

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Exception handlers: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь exception, handler и endpoint.
```

Это публичный starter contract практики «Domain exception handler». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Leaking `str(database_error)` to clients exposes schema/SQL details and creates an unstable contract.

## Practice

**A · Code/result prediction.** Change one input in the `domain exception` example and predict the result before running it.

**B · Find the bug.** Find code that violates `HTTP mapping` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `domain exception` and add one edge-case test.

**E · Interview explanation.** Explain Exception handlers in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Exception handlers и как это работает?

### Follow-up

Какая типичная ошибка связана с Exception handlers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

An exception handler translates an exception type into a consistent HTTP response at an application/router boundary.

### Нормальный Junior answer

> An exception handler translates an exception type into a consistent HTTP response at an application/router boundary. Domain code raises a meaningful domain exception; FastAPI handler maps it to status and safe payload while unexpected errors remain server failures. Важное ограничение: Do not catch every exception and convert programming bugs into 400 responses.

### Углубление / follow-up

**Какая типичная ошибка связана с Exception handlers?**

Leaking `str(database_error)` to clients exposes schema/SQL details and creates an unstable contract.

## Expected answer rubric

### Must mention

- domain exception
- HTTP mapping
- global handler
- avoid leaking internals

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Leaking `str(database_error)` to clients exposes schema/SQL details and creates an unstable contract.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Exception handlers?

## Задача

### Domain exception handler

DomainConflict handler возвращает status 409 и JSON error; GET /conflict поднимает already booked.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** An exception handler translates an exception type into a consistent HTTP response at an application/router boundary.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Leaking `str(database_error)` to clients exposes schema/SQL details and creates an unstable contract.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
