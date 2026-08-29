# Cookies

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cookies**, а не только запомнить термин;
- прочитать и изменить короткий пример для `request/response headers`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A cookie is a name/value set by response header and automatically returned by a browser according to domain, path, expiry and security attributes.

### Как работает

HttpOnly blocks JavaScript reads, Secure restricts HTTPS transport and SameSite limits cross-site sending; none replaces server-side authorization.


### Важный нюанс / limitation

Cookie authentication needs CSRF considerations because the browser attaches cookies automatically.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- request/response headers
- domain/path
- expiration
- HttpOnly

### Полезно

- Secure
- SameSite

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Cookies: отдельный пример

```http
GET /examples/s12_cookies HTTP/1.1
Accept: application/json
X-Request-ID: req-12-11
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Cookies».

## Common mistakes

### Ошибка 1

Putting a session cookie without HttpOnly/Secure/SameSite defaults unnecessarily expands the attack surface.

## Practice

**A · Code/result prediction.** Change one input in the `request/response headers` example and predict the result before running it.

**B · Find the bug.** Find code that violates `domain/path` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `request/response headers` and add one edge-case test.

**E · Interview explanation.** Explain Cookies in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Cookies и как это работает?

### Follow-up

Какая типичная ошибка связана с Cookies?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A cookie is a name/value set by response header and automatically returned by a browser according to domain, path, expiry and security attributes.

### Нормальный Junior answer

> A cookie is a name/value set by response header and automatically returned by a browser according to domain, path, expiry and security attributes. HttpOnly blocks JavaScript reads, Secure restricts HTTPS transport and SameSite limits cross-site sending; none replaces server-side authorization. Важное ограничение: Cookie authentication needs CSRF considerations because the browser attaches cookies automatically.

### Углубление / follow-up

**Какая типичная ошибка связана с Cookies?**

Putting a session cookie without HttpOnly/Secure/SameSite defaults unnecessarily expands the attack surface.

## Expected answer rubric

### Must mention

- request/response headers
- domain/path
- expiration
- HttpOnly

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Putting a session cookie without HttpOnly/Secure/SameSite defaults unnecessarily expands the attack surface.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Cookies?

## Задача

Сделай короткую письменную практику по теме **Cookies**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A cookie is a name/value set by response header and automatically returned by a browser according to domain, path, expiry and security attributes.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Putting a session cookie without HttpOnly/Secure/SameSite defaults unnecessarily expands the attack surface.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
