# Response models

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Response models**, а не только запомнить термин;
- прочитать и изменить короткий пример для `contract`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A response model defines the public output schema and filters/serializes endpoint results.

### Как работает

FastAPI validates the returned value against the model and emits the declared representation in OpenAPI.


### Важный нюанс / limitation

Use a separate public schema so password hashes and internal flags cannot leak from an ORM object.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- contract
- serialization
- filtering fields
- avoiding secret leakage

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Response models: отдельный пример

```text
Сценарий: Endpoint возвращает ORM object вместе с password_hash.

Проверка:
Явная response model/DTO с allowlist полей; contract test проверяет отсутствие secret.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Returning ORM `__dict__` or an unrestricted model can expose secret/internal fields.

## Practice

**A · Code/result prediction.** Change one input in the `contract` example and predict the result before running it.

**B · Find the bug.** Find code that violates `serialization` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `contract` and add one edge-case test.

**E · Interview explanation.** Explain Response models in 45–60 seconds and include one limitation.

## Debugging practice

### Secret ORM field

**Сценарий:** Endpoint возвращает ORM object вместе с password_hash.

**Rubric:** Явная response model/DTO с allowlist полей; contract test проверяет отсутствие secret.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Response models и как это работает?

### Follow-up

Какая типичная ошибка связана с Response models?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A response model defines the public output schema and filters/serializes endpoint results.

### Нормальный Junior answer

> A response model defines the public output schema and filters/serializes endpoint results. FastAPI validates the returned value against the model and emits the declared representation in OpenAPI. Важное ограничение: Use a separate public schema so password hashes and internal flags cannot leak from an ORM object.

### Углубление / follow-up

**Какая типичная ошибка связана с Response models?**

Returning ORM `__dict__` or an unrestricted model can expose secret/internal fields.

## Expected answer rubric

### Must mention

- contract
- serialization
- filtering fields
- avoiding secret leakage

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning ORM `__dict__` or an unrestricted model can expose secret/internal fields.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Response models?

## Задача

### Не раскрыть secret

UserPublic response_model для GET /users/me должен удалить password_hash из handler result.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A response model defines the public output schema and filters/serializes endpoint results.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Returning ORM `__dict__` or an unrestricted model can expose secret/internal fields.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
