# Index mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Index mental model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `auxiliary data structure`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A database index is an auxiliary structure that can find ordered key ranges without scanning every table row.

### Как работает

It speeds matching access paths but consumes storage and adds work to INSERT/UPDATE/DELETE. The planner may choose a sequential scan when many rows match.


### Важный нюанс / limitation

Design indexes from actual WHERE/JOIN/ORDER patterns and inspect EXPLAIN ANALYZE; an index on every column is harmful.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Index mental model: отдельный пример

```text
Сценарий: Lookup по уникальному external_id замедлился после роста таблицы.

Проверка:
Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Adding an index without the query shape or selectivity can increase write cost while never being selected.

## Practice

**A · Code/result prediction.** Change one input in the `auxiliary data structure` example and predict the result before running it.

**B · Find the bug.** Find code that violates `faster reads` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `auxiliary data structure` and add one edge-case test.

**E · Interview explanation.** Explain Index mental model in 45–60 seconds and include one limitation.

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

## Interview questions

### Основной вопрос

Что такое Index mental model и как это работает?

### Follow-up

Какая типичная ошибка связана с Index mental model?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A database index is an auxiliary structure that can find ordered key ranges without scanning every table row.

### Нормальный Junior answer

> A database index is an auxiliary structure that can find ordered key ranges without scanning every table row. It speeds matching access paths but consumes storage and adds work to INSERT/UPDATE/DELETE. The planner may choose a sequential scan when many rows match. Важное ограничение: Design indexes from actual WHERE/JOIN/ORDER patterns and inspect EXPLAIN ANALYZE; an index on every column is harmful.

### Углубление / follow-up

**Какая типичная ошибка связана с Index mental model?**

Adding an index without the query shape or selectivity can increase write cost while never being selected.

## Expected answer rubric

### Must mention

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Adding an index without the query shape or selectivity can increase write cost while never being selected.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Index mental model?

## Задача

Сделай короткую письменную практику по теме **Index mental model**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A database index is an auxiliary structure that can find ordered key ranges without scanning every table row.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Adding an index without the query shape or selectivity can increase write cost while never being selected.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
