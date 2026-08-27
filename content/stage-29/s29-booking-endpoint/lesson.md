# Booking endpoint

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- объяснить `availability check` своими словами и связать с backend-сценарием;
- объяснить `transaction` своими словами и связать с backend-сценарием;
- объяснить `DB invariant` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Junior system design начинается с требований, request path, source of truth и failure modes.

В теме **Booking endpoint** важно уверенно объяснять следующие части:

### availability check

Для `availability check` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### transaction

Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

### DB invariant

Для `DB invariant` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### concurrent requests

Для `concurrent requests` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### idempotency

Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

### conflict response

Для `conflict response` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### notification

Для `notification` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```text
Client → reverse proxy → FastAPI → service → PostgreSQL
                                  ↘ Redis
                                  ↘ outbox → worker
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Начинать с microservices, не определив нагрузку, consistency и ownership.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Booking endpoint** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Уточни traffic, consistency, latency и failure behavior перед схемой компонентов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- availability check
- transaction
- DB invariant
- concurrent requests
- Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Начинать с microservices, не определив нагрузку, consistency и ownership.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- availability check
- transaction
- DB invariant
- concurrent requests
- idempotency
- conflict response
- notification.

## Задача

Разбери backend-сценарий: **Уточни traffic, consistency, latency и failure behavior перед схемой компонентов.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Architecture practice

### Booking endpoint

**Сценарий:** Спроектируй POST booking.

**Rubric:** Validation, auth, transaction, 201/409, idempotency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Booking endpoint**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
