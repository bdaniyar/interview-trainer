# Content negotiation and Content-Type

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Content negotiation and Content-Type**, а не только запомнить термин;
- прочитать и изменить короткий пример для `JSON`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`Content-Type` describes the representation sent in a body; `Accept` describes representations the client can receive.

### Как работает

For JSON APIs the sender normally uses `application/json`; charset matters for textual formats and body parsing follows the declared media type.


### Важный нюанс / limitation

A JSON-looking string with the wrong Content-Type is not the same protocol contract.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- JSON
- charset
- Accept

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Content negotiation and Content-Type: отдельный пример

```http
GET /examples/s12_content_negotiation_and_content_type HTTP/1.1
Accept: application/json
X-Request-ID: req-12-10
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Content negotiation and Content-Type».

## Common mistakes

### Ошибка 1

Confusing Accept with Content-Type produces 415/406 behavior or incorrect parsing.

## Practice

**A · Code/result prediction.** Change one input in the `JSON` example and predict the result before running it.

**B · Find the bug.** Find code that violates `charset` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `JSON` and add one edge-case test.

**E · Interview explanation.** Explain Content negotiation and Content-Type in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Content negotiation and Content-Type и как это работает?

### Follow-up

Какая типичная ошибка связана с Content negotiation and Content-Type?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`Content-Type` describes the representation sent in a body; `Accept` describes representations the client can receive.

### Нормальный Junior answer

> `Content-Type` describes the representation sent in a body; `Accept` describes representations the client can receive. For JSON APIs the sender normally uses `application/json`; charset matters for textual formats and body parsing follows the declared media type. Важное ограничение: A JSON-looking string with the wrong Content-Type is not the same protocol contract.

### Углубление / follow-up

**Какая типичная ошибка связана с Content negotiation and Content-Type?**

Confusing Accept with Content-Type produces 415/406 behavior or incorrect parsing.

## Expected answer rubric

### Must mention

- JSON
- charset
- Accept

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Confusing Accept with Content-Type produces 415/406 behavior or incorrect parsing.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Content negotiation and Content-Type?

## Задача

Сделай короткую письменную практику по теме **Content negotiation and Content-Type**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `Content-Type` describes the representation sent in a body; `Accept` describes representations the client can receive.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Confusing Accept with Content-Type produces 415/406 behavior or incorrect parsing.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
