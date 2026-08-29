# HTTP methods

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **HTTP methods**, а не только запомнить термин;
- прочитать и изменить короткий пример для `GET`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

HTTP methods express intent: GET reads, POST submits/creates/actions, PUT replaces at a known target, PATCH partially changes and DELETE removes.

### Как работает

Safety means no requested state change; idempotency means repeating the same request has the same intended effect. These are semantics, not automatic framework enforcement.


### Важный нюанс / limitation

POST can be made retry-safe with an idempotency key, while a badly designed PUT can still have extra side effects.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- GET
- POST
- PUT
- PATCH

### Полезно

- DELETE
- OPTIONS

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### HTTP methods: отдельный пример

```http
GET /examples/s12_http_methods HTTP/1.1
Accept: application/json
X-Request-ID: req-12-3
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «HTTP methods».

## Common mistakes

### Ошибка 1

Choosing a method only by whether it has a body ignores caching, retries and client expectations.

## Practice

**A · Code/result prediction.** Change one input in the `GET` example and predict the result before running it.

**B · Find the bug.** Find code that violates `POST` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `GET` and add one edge-case test.

**E · Interview explanation.** Explain HTTP methods in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое HTTP methods и как это работает?

### Follow-up

Какая типичная ошибка связана с HTTP methods?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

HTTP methods express intent: GET reads, POST submits/creates/actions, PUT replaces at a known target, PATCH partially changes and DELETE removes.

### Нормальный Junior answer

> HTTP methods express intent: GET reads, POST submits/creates/actions, PUT replaces at a known target, PATCH partially changes and DELETE removes. Safety means no requested state change; idempotency means repeating the same request has the same intended effect. These are semantics, not automatic framework enforcement. Важное ограничение: POST can be made retry-safe with an idempotency key, while a badly designed PUT can still have extra side effects.

### Углубление / follow-up

**Какая типичная ошибка связана с HTTP methods?**

Choosing a method only by whether it has a body ignores caching, retries and client expectations.

## Expected answer rubric

### Must mention

- GET
- POST
- PUT
- PATCH

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Choosing a method only by whether it has a body ignores caching, retries and client expectations.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с HTTP methods?

## Задача

Сделай короткую письменную практику по теме **HTTP methods**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** HTTP methods express intent: GET reads, POST submits/creates/actions, PUT replaces at a known target, PATCH partially changes and DELETE removes.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Choosing a method only by whether it has a body ignores caching, retries and client expectations.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
