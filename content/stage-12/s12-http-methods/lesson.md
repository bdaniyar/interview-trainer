# HTTP methods

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- объяснить `GET` своими словами и связать с backend-сценарием;
- объяснить `POST` своими словами и связать с backend-сценарием;
- объяснить `PUT` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

HTTP — контракт между клиентом и сервером: method, target, headers, body, status и cache semantics.

В теме **HTTP methods** важно уверенно объяснять следующие части:

### GET

Для `GET` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### POST

Для `POST` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### PUT

Для `PUT` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### PATCH

Для `PATCH` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### DELETE

Для `DELETE` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### OPTIONS

Для `OPTIONS` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### HEAD basics

Для `HEAD basics` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### HTTP methods: отдельный пример

```http
GET /examples/s12_http_methods HTTP/1.1
Accept: application/json
X-Request-ID: req-12-3
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «HTTP methods».

## Common mistakes

**Ошибка:** Возвращать 200 для любой ошибки или считать POST автоматически неидемпотентным при любом дизайне.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **HTTP methods** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Спроектируй request/response контракт и объясни retry, idempotency и error body. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- GET
- POST
- PUT
- PATCH
- Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Возвращать 200 для любой ошибки или считать POST автоматически неидемпотентным при любом дизайне.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS
- HEAD basics.

## Задача

Разбери backend-сценарий: **Спроектируй request/response контракт и объясни retry, idempotency и error body.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **HTTP methods**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
