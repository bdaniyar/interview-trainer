# HTTP/HTTPS and TLS basics

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **HTTP/HTTPS and TLS basics**, а не только запомнить термин;
- прочитать и изменить короткий пример для `encryption`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

HTTPS is HTTP carried through TLS, providing encryption in transit, integrity and server authentication through certificates.

### Как работает

A TLS handshake negotiates keys and verifies the certificate chain; a reverse proxy may terminate TLS before forwarding to the app on a trusted network.


### Важный нюанс / limitation

HTTPS does not validate business permissions or encrypt data at rest.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- encryption
- authentication
- certificate
- TLS termination

### Полезно

- no cryptography deep dive

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### HTTP/HTTPS and TLS basics: отдельный пример

```http
GET /examples/s12_http_https_and_tls_basics HTTP/1.1
Accept: application/json
X-Request-ID: req-12-13
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «HTTP/HTTPS and TLS basics».

## Common mistakes

### Ошибка 1

Trusting forwarded scheme/client headers from arbitrary peers can make an app believe an insecure request was HTTPS.

## Practice

**A · Code/result prediction.** Change one input in the `encryption` example and predict the result before running it.

**B · Find the bug.** Find code that violates `authentication` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `encryption` and add one edge-case test.

**E · Interview explanation.** Explain HTTP/HTTPS and TLS basics in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое HTTP/HTTPS and TLS basics и как это работает?

### Follow-up

Какая типичная ошибка связана с HTTP/HTTPS and TLS basics?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

HTTPS is HTTP carried through TLS, providing encryption in transit, integrity and server authentication through certificates.

### Нормальный Junior answer

> HTTPS is HTTP carried through TLS, providing encryption in transit, integrity and server authentication through certificates. A TLS handshake negotiates keys and verifies the certificate chain; a reverse proxy may terminate TLS before forwarding to the app on a trusted network. Важное ограничение: HTTPS does not validate business permissions or encrypt data at rest.

### Углубление / follow-up

**Какая типичная ошибка связана с HTTP/HTTPS and TLS basics?**

Trusting forwarded scheme/client headers from arbitrary peers can make an app believe an insecure request was HTTPS.

## Expected answer rubric

### Must mention

- encryption
- authentication
- certificate
- TLS termination

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Trusting forwarded scheme/client headers from arbitrary peers can make an app believe an insecure request was HTTPS.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с HTTP/HTTPS and TLS basics?

## Задача

Сделай короткую письменную практику по теме **HTTP/HTTPS and TLS basics**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** HTTPS is HTTP carried through TLS, providing encryption in transit, integrity and server authentication through certificates.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Trusting forwarded scheme/client headers from arbitrary peers can make an app believe an insecure request was HTTPS.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
