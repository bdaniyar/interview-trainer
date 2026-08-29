# Cache invalidation

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `update/delete invalidation` своими словами и связать с backend-сценарием;
- объяснить `TTL` своими словами и связать с backend-сценарием;
- объяснить `stale cache` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Redis — быстрый in-memory data store для cache и временного состояния, но источник истины выбирается по durability requirements.

В теме **Cache invalidation** важно уверенно объяснять следующие части:

### update/delete invalidation

Для `update/delete invalidation` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### TTL

Для `TTL` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### stale cache

Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

### race windows

Window function считает значение по partition, не сворачивая строки как GROUP BY; порядок внутри `OVER` задаёт frame/ranking semantics.

### versioned keys

Для `versioned keys` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### GET обычно read-heavy и повторяемый

Для `GET обычно read-heavy и повторяемый` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### mutations меняют состояние

Для `mutations меняют состояние` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Cache invalidation: отдельный пример

```text
Сценарий: PUT commit успешен, GET отдаёт старое.

Проверка:
Invalidate/update after commit; key ownership, TTL, race.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Использовать Pub/Sub как историю или забыть TTL и invalidation.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Cache invalidation** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери cache miss, stale value, Redis outage и concurrent refill. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- update/delete invalidation
- TTL
- stale cache
- race windows
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

- update/delete invalidation
- TTL
- stale cache
- race windows
- versioned keys.
- GET обычно read-heavy и повторяемый
- mutations меняют состояние
- после mutation связанные read cache keys нужно invalidation/update

## Задача

Разбери backend-сценарий: **Разбери cache miss, stale value, Redis outage и concurrent refill.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Stale cache

**Сценарий:** PUT commit успешен, GET отдаёт старое.

**Rubric:** Invalidate/update after commit; key ownership, TTL, race.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Cache invalidation**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
