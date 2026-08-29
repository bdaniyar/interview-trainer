# Status codes

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Status codes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `200`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

HTTP status codes communicate the outcome category and specific result of processing a request.

### Как работает

Typical API codes include 200, 201 with Location where useful, 204 without body, 400 malformed request, 401 unauthenticated, 403 forbidden, 404, 409 conflict, 422 validation and 500 unexpected server error.


### Важный нюанс / limitation

Use one consistent error body with a machine-readable code; do not leak stack traces.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- 200
- 201
- 202
- 204

### Полезно

- 304
- 400

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Status codes: отдельный пример

```http
GET /examples/s12_status_codes HTTP/1.1
Accept: application/json
X-Request-ID: req-12-7
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Status codes».

## Common mistakes

### Ошибка 1

Returning 200 for every error forces clients to reverse-engineer success from response text.

## Practice

**A · Code/result prediction.** Change one input in the `200` example and predict the result before running it.

**B · Find the bug.** Find code that violates `201` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `200` and add one edge-case test.

**E · Interview explanation.** Explain Status codes in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Status codes и как это работает?

### Follow-up

Какая типичная ошибка связана с Status codes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

HTTP status codes communicate the outcome category and specific result of processing a request.

### Нормальный Junior answer

> HTTP status codes communicate the outcome category and specific result of processing a request. Typical API codes include 200, 201 with Location where useful, 204 without body, 400 malformed request, 401 unauthenticated, 403 forbidden, 404, 409 conflict, 422 validation and 500 unexpected server error. Важное ограничение: Use one consistent error body with a machine-readable code; do not leak stack traces.

### Углубление / follow-up

**Какая типичная ошибка связана с Status codes?**

Returning 200 for every error forces clients to reverse-engineer success from response text.

## Expected answer rubric

### Must mention

- 200
- 201
- 202
- 204

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning 200 for every error forces clients to reverse-engineer success from response text.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Status codes?

## Задача

Сделай короткую письменную практику по теме **Status codes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** HTTP status codes communicate the outcome category and specific result of processing a request.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Returning 200 for every error forces clients to reverse-engineer success from response text.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
