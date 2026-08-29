# Data structures

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `strings` своими словами и связать с backend-сценарием;
- объяснить `hashes` своими словами и связать с backend-сценарием;
- объяснить `lists` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Redis — быстрый in-memory data store для cache и временного состояния, но источник истины выбирается по durability requirements.

В теме **Data structures** важно уверенно объяснять следующие части:

### strings

Для `strings` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### hashes

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

### lists

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### sets

Для `sets` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### sorted sets

Для `sorted sets` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### streams awareness

Для `streams awareness` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Data structures: отдельный пример

```text
Сценарий: profile:42 разных tenants возвращает чужие данные.

Проверка:
Key включает namespace/version/tenant/entity; authorization остаётся server-side.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Использовать Pub/Sub как историю или забыть TTL и invalidation.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Data structures** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери cache miss, stale value, Redis outage и concurrent refill. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- strings
- hashes
- lists
- sets
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

- strings
- hashes
- lists
- sets
- sorted sets
- streams awareness.

## Задача

Разбери backend-сценарий: **Разбери cache miss, stale value, Redis outage и concurrent refill.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Cache key collision

**Сценарий:** profile:42 разных tenants возвращает чужие данные.

**Rubric:** Key включает namespace/version/tenant/entity; authorization остаётся server-side.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Data structures**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
