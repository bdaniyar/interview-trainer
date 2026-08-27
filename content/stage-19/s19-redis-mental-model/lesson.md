# Redis mental model

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `in-memory data structure server` своими словами и связать с backend-сценарием;
- объяснить `fast` своими словами и связать с backend-сценарием;
- объяснить `optional persistence modes` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Redis — быстрый in-memory data store для cache и временного состояния, но источник истины выбирается по durability requirements.

В теме **Redis mental model** важно уверенно объяснять следующие части:

### in-memory data structure server

Для `in-memory data structure server` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### fast

Для `fast` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

### optional persistence modes

`T | None` разрешает значение `None`, но не делает аргумент или поле необязательным без default; missing и explicit null — разные состояния.

### not a relational source of truth by default

Для `not a relational source of truth by default` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```text
GET cache:user:42 → miss
SELECT user FROM PostgreSQL
SET cache:user:42 value EX 60
UPDATE user → COMMIT → DEL cache:user:42
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Использовать Pub/Sub как историю или забыть TTL и invalidation.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Redis mental model** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери cache miss, stale value, Redis outage и concurrent refill. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- in-memory data structure server
- fast
- optional persistence modes
- not a relational source of truth by default.
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

- in-memory data structure server
- fast
- optional persistence modes
- not a relational source of truth by default.

## Задача

Разбери backend-сценарий: **Разбери cache miss, stale value, Redis outage и concurrent refill.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Redis mental model**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
