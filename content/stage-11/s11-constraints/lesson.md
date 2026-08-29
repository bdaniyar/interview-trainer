# Constraints

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Constraints**, а не только запомнить термин;
- прочитать и изменить короткий пример для `NOT NULL`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Database constraints enforce invariants for every writer: NOT NULL, UNIQUE, CHECK, primary/foreign keys.

### Как работает

The database evaluates constraints during writes/transaction completion and rejects invalid state; application code translates the specific conflict.


### Важный нюанс / limitation

Validation improves UX but cannot replace a DB constraint under concurrent requests.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- NOT NULL
- UNIQUE
- CHECK
- FK

### Полезно

- business invariant in DB

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Constraints: отдельный пример

```sql
-- 11.2 · Constraints
-- Focus: NOT NULL, UNIQUE, CHECK, FK
SELECT 's11_constraints' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Checking uniqueness only with SELECT then INSERT races; a UNIQUE constraint must be the final authority.

## Practice

**A · Code/result prediction.** Change one input in the `NOT NULL` example and predict the result before running it.

**B · Find the bug.** Find code that violates `UNIQUE` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `NOT NULL` and add one edge-case test.

**E · Interview explanation.** Explain Constraints in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Constraints и как это работает?

### Follow-up

Какая типичная ошибка связана с Constraints?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Database constraints enforce invariants for every writer: NOT NULL, UNIQUE, CHECK, primary/foreign keys.

### Нормальный Junior answer

> Database constraints enforce invariants for every writer: NOT NULL, UNIQUE, CHECK, primary/foreign keys. The database evaluates constraints during writes/transaction completion and rejects invalid state; application code translates the specific conflict. Важное ограничение: Validation improves UX but cannot replace a DB constraint under concurrent requests.

### Углубление / follow-up

**Какая типичная ошибка связана с Constraints?**

Checking uniqueness only with SELECT then INSERT races; a UNIQUE constraint must be the final authority.

## Expected answer rubric

### Must mention

- NOT NULL
- UNIQUE
- CHECK
- FK

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Checking uniqueness only with SELECT then INSERT races; a UNIQUE constraint must be the final authority.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Constraints?

## Задача

Сделай короткую письменную практику по теме **Constraints**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Database constraints enforce invariants for every writer: NOT NULL, UNIQUE, CHECK, primary/foreign keys.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Checking uniqueness only with SELECT then INSERT races; a UNIQUE constraint must be the final authority.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
