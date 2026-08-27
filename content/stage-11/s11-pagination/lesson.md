# Pagination

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- объяснить `OFFSET/LIMIT` своими словами и связать с backend-сценарием;
- объяснить `large-offset cost` своими словами и связать с backend-сценарием;
- объяснить `cursor/keyset pagination` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

PostgreSQL обеспечивает ограничения и конкурентную работу ближе к данным; индекс и transaction boundary проектируются под запросы и инварианты.

В теме **Pagination** важно уверенно объяснять следующие части:

### OFFSET/LIMIT

Для `OFFSET/LIMIT` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### large-offset cost

Для `large-offset cost` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### cursor/keyset pagination

Для `cursor/keyset pagination` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

### stable ordering

Для `stable ordering` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```sql
BEGIN;
SELECT id FROM rooms WHERE id = 42 FOR UPDATE;
INSERT INTO bookings(room_id, starts_at, ends_at) VALUES (42, $1, $2);
COMMIT;
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Pagination** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови инвариант, конкурентный сценарий и точку, где его гарантирует база. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- OFFSET/LIMIT
- large-offset cost
- cursor/keyset pagination
- stable ordering.
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

- OFFSET/LIMIT
- large-offset cost
- cursor/keyset pagination
- stable ordering.

## Задача

Разбери backend-сценарий: **Назови инвариант, конкурентный сценарий и точку, где его гарантирует база.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Pagination**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
