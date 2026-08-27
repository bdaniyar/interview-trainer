# PUT vs PATCH

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- объяснить `replacement vs partial update` своими словами и связать с backend-сценарием;
- объяснить `API contract` своими словами и связать с backend-сценарием;
- объяснить `idempotency.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

HTTP — контракт между клиентом и сервером: method, target, headers, body, status и cache semantics.

В теме **PUT vs PATCH** важно уверенно объяснять следующие части:

### replacement vs partial update

Для `replacement vs partial update` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### API contract

Для `API contract` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.

### idempotency

Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```http
PATCH /users/42 HTTP/1.1
Content-Type: application/json
If-Match: "user-v7"

{"display_name": "Aida"}
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Возвращать 200 для любой ошибки или считать POST автоматически неидемпотентным при любом дизайне.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **PUT vs PATCH** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Спроектируй request/response контракт и объясни retry, idempotency и error body. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- replacement vs partial update
- API contract
- idempotency.
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

- replacement vs partial update
- API contract
- idempotency.

## Задача

Разбери backend-сценарий: **Спроектируй request/response контракт и объясни retry, idempotency и error body.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **PUT vs PATCH**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
