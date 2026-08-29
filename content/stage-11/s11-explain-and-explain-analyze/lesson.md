# EXPLAIN and EXPLAIN ANALYZE

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **EXPLAIN and EXPLAIN ANALYZE**, а не только запомнить термин;
- прочитать и изменить короткий пример для `estimated vs actual`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`EXPLAIN` shows the planned operations and estimates; `EXPLAIN ANALYZE` executes the statement and adds actual rows/timing.

### Как работает

Read plan nodes from children upward and compare estimated vs actual rows, loops, scan type and buffers when requested.


### Важный нюанс / limitation

ANALYZE really executes data-changing statements unless wrapped and rolled back; test safely.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- estimated vs actual
- scan types
- rows
- loops

### Полезно

- timing
- ANALYZE executes the query

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### EXPLAIN and EXPLAIN ANALYZE: отдельный пример

```text
Сценарий: Planner выбирает Seq Scan для boolean active, хотя index существует.

Проверка:
При высокой доле совпадений Seq Scan может быть дешевле; сравнить estimates/actual rows, не принуждать index вслепую.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Looking only at total time misses a severe estimate error or loop count that becomes expensive on larger data.

## Practice

**A · Code/result prediction.** Change one input in the `estimated vs actual` example and predict the result before running it.

**B · Find the bug.** Find code that violates `scan types` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `estimated vs actual` and add one edge-case test.

**E · Interview explanation.** Explain EXPLAIN and EXPLAIN ANALYZE in 45–60 seconds and include one limitation.

## SQL practice

### Sequential scan

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

**Вопрос:** После роста таблицы endpoint замедлился и plan показывает Seq Scan. План диагностики?

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### Low-selectivity index

**Сценарий:** Planner выбирает Seq Scan для boolean active, хотя index существует.

**Rubric:** При высокой доле совпадений Seq Scan может быть дешевле; сравнить estimates/actual rows, не принуждать index вслепую.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое EXPLAIN and EXPLAIN ANALYZE и как это работает?

### Follow-up

Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`EXPLAIN` shows the planned operations and estimates; `EXPLAIN ANALYZE` executes the statement and adds actual rows/timing.

### Нормальный Junior answer

> `EXPLAIN` shows the planned operations and estimates; `EXPLAIN ANALYZE` executes the statement and adds actual rows/timing. Read plan nodes from children upward and compare estimated vs actual rows, loops, scan type and buffers when requested. Важное ограничение: ANALYZE really executes data-changing statements unless wrapped and rolled back; test safely.

### Углубление / follow-up

**Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?**

Looking only at total time misses a severe estimate error or loop count that becomes expensive on larger data.

## Expected answer rubric

### Must mention

- estimated vs actual
- scan types
- rows
- loops

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Looking only at total time misses a severe estimate error or loop count that becomes expensive on larger data.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?

## Задача

Сделай короткую письменную практику по теме **EXPLAIN and EXPLAIN ANALYZE**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `EXPLAIN` shows the planned operations and estimates; `EXPLAIN ANALYZE` executes the statement and adds actual rows/timing.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Looking only at total time misses a severe estimate error or loop count that becomes expensive on larger data.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
