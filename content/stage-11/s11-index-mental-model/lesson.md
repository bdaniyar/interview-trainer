# Index mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- объяснить `auxiliary data structure` своими словами и связать с backend-сценарием;
- объяснить `faster reads` своими словами и связать с backend-сценарием;
- объяснить `storage/write cost` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

PostgreSQL обеспечивает ограничения и конкурентную работу ближе к данным; индекс и transaction boundary проектируются под запросы и инварианты.

В теме **Index mental model** важно уверенно объяснять следующие части:

### auxiliary data structure

Для `auxiliary data structure` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### faster reads

Для `faster reads` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### storage/write cost

Для `storage/write cost` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### index is not magic

Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Index mental model: отдельный пример

```text
Сценарий: Lookup по уникальному external_id замедлился после роста таблицы.

Проверка:
Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Index mental model** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови инвариант, конкурентный сценарий и точку, где его гарантирует база. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic.
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

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic.

## Задача

Разбери backend-сценарий: **Назови инвариант, конкурентный сценарий и точку, где его гарантирует база.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## SQL practice

### Index для email lookup

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

**Вопрос:** GET /users/by-email выполняет WHERE lower(email)=lower($1), но индекс только на email. Что проверить?

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### Missing index

**Сценарий:** Lookup по уникальному external_id замедлился после роста таблицы.

**Rubric:** Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Index mental model**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
