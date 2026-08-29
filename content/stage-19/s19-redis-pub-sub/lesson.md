# Redis Pub/Sub

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `publisher` своими словами и связать с backend-сценарием;
- объяснить `subscriber` своими словами и связать с backend-сценарием;
- объяснить `channel` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Redis — быстрый in-memory data store для cache и временного состояния, но источник истины выбирается по durability requirements.

В теме **Redis Pub/Sub** важно уверенно объяснять следующие части:

### publisher

Для `publisher` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### subscriber

Для `subscriber` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### channel

Для `channel` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### live delivery

Для `live delivery` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### no durable history

Для `no durable history` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### offline subscriber misses message

Для `offline subscriber misses message` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### no acknowledgement/replay

Для `no acknowledgement/replay` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Redis Pub/Sub: отдельный пример

```text
Сценарий: Offline WebSocket client потерял события.

Проверка:
Pub/Sub только live fan-out; durable history/read state хранить в PostgreSQL или durable stream.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Использовать Pub/Sub как историю или забыть TTL и invalidation.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Redis Pub/Sub** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери cache miss, stale value, Redis outage и concurrent refill. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- publisher
- subscriber
- channel
- live delivery
- Для cache всегда определяй key, value, TTL, invalidation и fallback.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Использовать Pub/Sub как историю или забыть TTL и invalidation.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- publisher
- subscriber
- channel
- live delivery
- no durable history
- offline subscriber misses message
- no acknowledgement/replay.

## Задача

Разбери backend-сценарий: **Разбери cache miss, stale value, Redis outage и concurrent refill.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### PubSub as history

**Сценарий:** Offline WebSocket client потерял события.

**Rubric:** Pub/Sub только live fan-out; durable history/read state хранить в PostgreSQL или durable stream.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Redis Pub/Sub**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
