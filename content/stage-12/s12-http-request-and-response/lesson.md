# HTTP request and response

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **HTTP request and response**, а не только запомнить термин;
- прочитать и изменить короткий пример для `start line`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

HTTP is a request/response application protocol: a request contains method, target, headers and optional body; a response contains status, headers and optional body.

### Как работает

The server parses the request, routes it, applies application logic and serializes a response. HTTP semantics remain distinct from JSON and framework implementation.


### Важный нюанс / limitation

Transport success does not mean business success; status and body must describe the application result.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- start line
- method
- path
- headers

### Полезно

- body
- status

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### HTTP request and response: отдельный пример

```http
GET /examples/s12_http_request_and_response HTTP/1.1
Accept: application/json
X-Request-ID: req-12-1
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «HTTP request and response».

## Common mistakes

### Ошибка 1

Returning 200 with an error hidden in JSON breaks clients, monitoring and standard retry/cache behavior.

## Practice

**A · Code/result prediction.** Change one input in the `start line` example and predict the result before running it.

**B · Find the bug.** Find code that violates `method` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `start line` and add one edge-case test.

**E · Interview explanation.** Explain HTTP request and response in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое HTTP request and response и как это работает?

### Follow-up

Какая типичная ошибка связана с HTTP request and response?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

HTTP is a request/response application protocol: a request contains method, target, headers and optional body; a response contains status, headers and optional body.

### Нормальный Junior answer

> HTTP is a request/response application protocol: a request contains method, target, headers and optional body; a response contains status, headers and optional body. The server parses the request, routes it, applies application logic and serializes a response. HTTP semantics remain distinct from JSON and framework implementation. Важное ограничение: Transport success does not mean business success; status and body must describe the application result.

### Углубление / follow-up

**Какая типичная ошибка связана с HTTP request and response?**

Returning 200 with an error hidden in JSON breaks clients, monitoring and standard retry/cache behavior.

## Expected answer rubric

### Must mention

- start line
- method
- path
- headers

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning 200 with an error hidden in JSON breaks clients, monitoring and standard retry/cache behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с HTTP request and response?

## Задача

Сделай короткую письменную практику по теме **HTTP request and response**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** HTTP is a request/response application protocol: a request contains method, target, headers and optional body; a response contains status, headers and optional body.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Returning 200 with an error hidden in JSON breaks clients, monitoring and standard retry/cache behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
