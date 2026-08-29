# Isolation levels

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Isolation levels**, а не только запомнить термин;
- прочитать и изменить короткий пример для `read committed`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Isolation levels define which effects of concurrent transactions can be observed.

### Как работает

PostgreSQL commonly uses Read Committed per statement; Repeatable Read keeps a transaction snapshot; Serializable may abort a transaction to preserve serial behavior.


### Важный нюанс / limitation

Higher isolation is not free and serialization failures require retry of the entire transaction.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- read committed
- repeatable read
- serializable
- anomalies at reasonable depth

### Полезно

- PostgreSQL-specific behavior

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Isolation levels: отдельный пример

```sql
-- 11.10 · Isolation levels
-- Focus: read committed, repeatable read, serializable, anomalies at reasonable depth
SELECT 's11_isolation_levels' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Changing isolation without identifying the anomaly often adds contention while leaving the actual invariant unprotected.

## Practice

**A · Code/result prediction.** Change one input in the `read committed` example and predict the result before running it.

**B · Find the bug.** Find code that violates `repeatable read` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `read committed` and add one edge-case test.

**E · Interview explanation.** Explain Isolation levels in 45–60 seconds and include one limitation.

## SQL practice

### Isolation anomaly

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

**Вопрос:** Две transaction читают доступный balance и обе списывают средства. Что гарантирует Read Committed?

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое Isolation levels и как это работает?

### Follow-up

Какая типичная ошибка связана с Isolation levels?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Isolation levels define which effects of concurrent transactions can be observed.

### Нормальный Junior answer

> Isolation levels define which effects of concurrent transactions can be observed. PostgreSQL commonly uses Read Committed per statement; Repeatable Read keeps a transaction snapshot; Serializable may abort a transaction to preserve serial behavior. Важное ограничение: Higher isolation is not free and serialization failures require retry of the entire transaction.

### Углубление / follow-up

**Какая типичная ошибка связана с Isolation levels?**

Changing isolation without identifying the anomaly often adds contention while leaving the actual invariant unprotected.

## Expected answer rubric

### Must mention

- read committed
- repeatable read
- serializable
- anomalies at reasonable depth

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Changing isolation without identifying the anomaly often adds contention while leaving the actual invariant unprotected.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Isolation levels?

## Задача

Сделай короткую письменную практику по теме **Isolation levels**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Isolation levels define which effects of concurrent transactions can be observed.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Changing isolation without identifying the anomaly often adds contention while leaving the actual invariant unprotected.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
