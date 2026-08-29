# Composite indexes and column order

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- объяснить `leftmost prefix intuition` своими словами и связать с backend-сценарием;
- объяснить `filter/order patterns` своими словами и связать с backend-сценарием;
- объяснить `equality before range as a heuristic, not dogma.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

PostgreSQL обеспечивает ограничения и конкурентную работу ближе к данным; индекс и transaction boundary проектируются под запросы и инварианты.

В теме **Composite indexes and column order** важно уверенно объяснять следующие части:

### leftmost prefix intuition

Router prefix добавляется ко всем путям группы и позволяет собирать модульный API без повторения `/users` или `/v1` в каждом decorator.

### filter/order patterns

Для `filter/order patterns` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### equality before range as a heuristic, not dogma

Для `equality before range as a heuristic, not dogma` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Composite indexes and column order: отдельный пример

```sql
-- 11.6 · Composite indexes and column order
-- Focus: leftmost prefix intuition, filter/order patterns, equality before range as a heuristic, not dogma
SELECT 's11_composite_indexes_and_column_order' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

**Ошибка:** Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Composite indexes and column order** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови инвариант, конкурентный сценарий и точку, где его гарантирует база. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- leftmost prefix intuition
- filter/order patterns
- equality before range as a heuristic, not dogma.
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

- leftmost prefix intuition
- filter/order patterns
- equality before range as a heuristic, not dogma.

## Задача

Разбери backend-сценарий: **Назови инвариант, конкурентный сценарий и точку, где его гарантирует база.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## SQL practice

### Composite index order

```sql
CREATE TABLE rooms (
    id bigint PRIMARY KEY,
    hotel_id bigint NOT NULL,
    number text NOT NULL,
    UNIQUE (hotel_id, number)
);
CREATE TABLE bookings (
    id bigint PRIMARY KEY,
    room_id bigint NOT NULL REFERENCES rooms(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL,
    CHECK (ends_at > starts_at)
);
```

Seed:

```sql
INSERT INTO rooms VALUES (1,10,'101'),(2,10,'102');
INSERT INTO bookings VALUES
(1,1,'2026-09-01','2026-09-05','confirmed'),
(2,1,'2026-09-10','2026-09-12','cancelled');
```

**Вопрос:** Запрос WHERE hotel_id=$1 AND starts_at >= $2 ORDER BY starts_at. Предложи индекс.

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Composite indexes and column order**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
