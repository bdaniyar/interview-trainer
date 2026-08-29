# Booking concurrency

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- объяснить `check-then-insert race` своими словами и связать с backend-сценарием;
- объяснить `unique/exclusion constraint` своими словами и связать с backend-сценарием;
- объяснить `conditional update` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

PostgreSQL обеспечивает ограничения и конкурентную работу ближе к данным; индекс и transaction boundary проектируются под запросы и инварианты.

В теме **Booking concurrency** важно уверенно объяснять следующие части:

### check-then-insert race

Для `check-then-insert race` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### unique/exclusion constraint

Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

### conditional update

Для `conditional update` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### row/advisory locks

Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

### transaction

Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

### `409 Conflict`

Для ``409 Conflict`` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Booking concurrency: отдельный пример

```sql
-- 11.17 · Booking concurrency
-- Focus: check-then-insert race, unique/exclusion constraint, conditional update, row/advisory locks
SELECT 's11_booking_concurrency' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

**Ошибка:** Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Booking concurrency** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови инвариант, конкурентный сценарий и точку, где его гарантирует база. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- check-then-insert race
- unique/exclusion constraint
- conditional update
- row/advisory locks
- Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- check-then-insert race
- unique/exclusion constraint
- conditional update
- row/advisory locks
- transaction
- `409 Conflict`.

## Задача

Разбери backend-сценарий: **Назови инвариант, конкурентный сценарий и точку, где его гарантирует база.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Booking concurrency**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
