# Normalization

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Normalization**, а не только запомнить термин;
- прочитать и изменить короткий пример для `duplication`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Normalization structures relations to reduce duplicated facts and update anomalies; Junior depth focuses on practical 1NF–3NF intuition.

### Как работает

Separate entities and connect them by keys so one fact has one authoritative storage location. Denormalization intentionally duplicates derived/read data for a measured need.


### Важный нюанс / limitation

Normalization is not maximum table count; boundaries follow data meaning and update dependencies.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- duplication
- update anomalies
- 1NF/2NF/3NF at practical Junior depth
- deliberate denormalization only with reason

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Normalization: отдельный пример

```sql
-- 11.3 · Normalization
-- Focus: duplication, update anomalies, 1NF/2NF/3NF at practical Junior depth, deliberate denormalization only with reason
SELECT 's11_normalization' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Storing the same user email in many order rows makes updates inconsistent and obscures the source of truth.

## Practice

**A · Code/result prediction.** Change one input in the `duplication` example and predict the result before running it.

**B · Find the bug.** Find code that violates `update anomalies` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `duplication` and add one edge-case test.

**E · Interview explanation.** Explain Normalization in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Normalization и как это работает?

### Follow-up

Какая типичная ошибка связана с Normalization?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Normalization structures relations to reduce duplicated facts and update anomalies; Junior depth focuses on practical 1NF–3NF intuition.

### Нормальный Junior answer

> Normalization structures relations to reduce duplicated facts and update anomalies; Junior depth focuses on practical 1NF–3NF intuition. Separate entities and connect them by keys so one fact has one authoritative storage location. Denormalization intentionally duplicates derived/read data for a measured need. Важное ограничение: Normalization is not maximum table count; boundaries follow data meaning and update dependencies.

### Углубление / follow-up

**Какая типичная ошибка связана с Normalization?**

Storing the same user email in many order rows makes updates inconsistent and obscures the source of truth.

## Expected answer rubric

### Must mention

- duplication
- update anomalies
- 1NF/2NF/3NF at practical Junior depth
- deliberate denormalization only with reason

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Storing the same user email in many order rows makes updates inconsistent and obscures the source of truth.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Normalization?

## Задача

Сделай короткую письменную практику по теме **Normalization**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Normalization structures relations to reduce duplicated facts and update anomalies; Junior depth focuses on practical 1NF–3NF intuition.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Storing the same user email in many order rows makes updates inconsistent and obscures the source of truth.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
