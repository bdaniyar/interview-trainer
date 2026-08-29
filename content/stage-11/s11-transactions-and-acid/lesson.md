# Transactions and ACID

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Transactions and ACID**, а не только запомнить термин;
- прочитать и изменить короткий пример для `atomicity`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A transaction groups operations into one atomic boundary; ACID describes atomicity, consistency, isolation and durability.

### Как работает

Commit makes the transaction's changes durable/visible under DB rules; rollback discards them. Consistency comes from correct code plus constraints, not the letter C automatically.


### Важный нюанс / limitation

Keep transactions short and avoid network calls while locks/resources are held.

### Где используется в backend

A service operation that creates an order and reserves inventory should commit or rollback as one unit where invariants require it.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- atomicity
- consistency
- isolation
- durability

### Полезно

- transaction boundary

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Transactions and ACID: отдельный пример

```text
Сценарий: Request держит transaction открытой во время HTTP-вызова.

Проверка:
Сетевой I/O вынести за DB transaction; короткая boundary уменьшает locks, pool pressure и stale snapshot.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Committing inside each repository call can leave half a use case saved after a later failure.

## Practice

**A · Code/result prediction.** Change one input in the `atomicity` example and predict the result before running it.

**B · Find the bug.** Find code that violates `consistency` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `atomicity` and add one edge-case test.

**E · Interview explanation.** Explain Transactions and ACID in 45–60 seconds and include one limitation.

## SQL practice

### Atomic booking

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

**Вопрос:** Два запроса бронируют последний room одновременно. Где защитить инвариант?

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### Long transaction

**Сценарий:** Request держит transaction открытой во время HTTP-вызова.

**Rubric:** Сетевой I/O вынести за DB transaction; короткая boundary уменьшает locks, pool pressure и stale snapshot.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Double booking race

**Сценарий:** Два SELECT видят свободный номер и создают booking.

**Rubric:** Защитить invariant в БД constraint/lock/conditional write и проверить concurrent integration test.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Transactions and ACID и как это работает?

### Follow-up

Какая типичная ошибка связана с Transactions and ACID?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A transaction groups operations into one atomic boundary; ACID describes atomicity, consistency, isolation and durability.

### Нормальный Junior answer

> A transaction groups operations into one atomic boundary; ACID describes atomicity, consistency, isolation and durability. Commit makes the transaction's changes durable/visible under DB rules; rollback discards them. Consistency comes from correct code plus constraints, not the letter C automatically. Важное ограничение: Keep transactions short and avoid network calls while locks/resources are held.

### Углубление / follow-up

**Какая типичная ошибка связана с Transactions and ACID?**

Committing inside each repository call can leave half a use case saved after a later failure.

## Expected answer rubric

### Must mention

- atomicity
- consistency
- isolation
- durability

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Committing inside each repository call can leave half a use case saved after a later failure.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Transactions and ACID?

## Задача

Сделай короткую письменную практику по теме **Transactions and ACID**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A transaction groups operations into one atomic boundary; ACID describes atomicity, consistency, isolation and durability.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Committing inside each repository call can leave half a use case saved after a later failure.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
