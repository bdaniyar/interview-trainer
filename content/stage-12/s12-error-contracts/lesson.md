# Error contracts

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Error contracts**, а не только запомнить термин;
- прочитать и изменить короткий пример для `stable shape`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

An API error contract is a stable response shape for failures, usually containing a machine code, human message and optional field details.

### Как работает

Domain/infrastructure exceptions are translated at the boundary to an appropriate status and safe payload; internal trace and secrets remain in protected logs.


### Важный нюанс / limitation

Clients should branch on stable code/status, not exact human wording.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- stable shape
- machine-readable code
- human message
- field errors

### Полезно

- no internal traces

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Error contracts: отдельный пример

```http
GET /examples/s12_error_contracts HTTP/1.1
Accept: application/json
X-Request-ID: req-12-20
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Error contracts».

## Common mistakes

### Ошибка 1

Returning raw exception strings leaks implementation details and creates an unstable public contract.

## Practice

**A · Code/result prediction.** Change one input in the `stable shape` example and predict the result before running it.

**B · Find the bug.** Find code that violates `machine-readable code` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `stable shape` and add one edge-case test.

**E · Interview explanation.** Explain Error contracts in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Error contracts и как это работает?

### Follow-up

Какая типичная ошибка связана с Error contracts?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

An API error contract is a stable response shape for failures, usually containing a machine code, human message and optional field details.

### Нормальный Junior answer

> An API error contract is a stable response shape for failures, usually containing a machine code, human message and optional field details. Domain/infrastructure exceptions are translated at the boundary to an appropriate status and safe payload; internal trace and secrets remain in protected logs. Важное ограничение: Clients should branch on stable code/status, not exact human wording.

### Углубление / follow-up

**Какая типичная ошибка связана с Error contracts?**

Returning raw exception strings leaks implementation details and creates an unstable public contract.

## Expected answer rubric

### Must mention

- stable shape
- machine-readable code
- human message
- field errors

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning raw exception strings leaks implementation details and creates an unstable public contract.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Error contracts?

## Задача

Сделай короткую письменную практику по теме **Error contracts**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** An API error contract is a stable response shape for failures, usually containing a machine code, human message and optional field details.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Returning raw exception strings leaks implementation details and creates an unstable public contract.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
