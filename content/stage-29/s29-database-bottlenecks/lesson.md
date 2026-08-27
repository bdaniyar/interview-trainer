# Database bottlenecks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- объяснить `slow query` своими словами и связать с backend-сценарием;
- объяснить `missing index` своими словами и связать с backend-сценарием;
- объяснить `N+1` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Junior system design начинается с требований, request path, source of truth и failure modes.

В теме **Database bottlenecks** важно уверенно объяснять следующие части:

### slow query

Для `slow query` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### missing index

Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

### N+1

N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой.

### too many connections

Для `too many connections` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

### lock contention

Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

### measure first

Для `measure first` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.

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

1. Объясни **Database bottlenecks** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Уточни traffic, consistency, latency и failure behavior перед схемой компонентов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- slow query
- missing index
- N+1
- too many connections
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

- slow query
- missing index
- N+1
- too many connections
- lock contention
- measure first.

## Задача

Разбери backend-сценарий: **Уточни traffic, consistency, latency и failure behavior перед схемой компонентов.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Architecture practice

### DB bottleneck

**Сценарий:** p95 вырос, DB CPU высокий.

**Rubric:** Slow queries, pool, plans, indexes, N+1.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Database bottlenecks**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
