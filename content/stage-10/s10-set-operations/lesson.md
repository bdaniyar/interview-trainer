# Set operations

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- объяснить ``UNION`` своими словами и связать с backend-сценарием;
- объяснить ``UNION ALL`` своими словами и связать с backend-сценарием;
- объяснить ``INTERSECT`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

SQL описывает требуемый набор строк; корректность начинается с cardinality, NULL semantics и явного порядка.

В теме **Set operations** важно уверенно объяснять следующие части:

### `UNION`

Для ``UNION`` сначала определи grain/cardinality результата, затем NULL и ordering semantics.

### `UNION ALL`

Для ``UNION ALL`` сначала определи grain/cardinality результата, затем NULL и ordering semantics.

### `INTERSECT`

Для ``INTERSECT`` сначала определи grain/cardinality результата, затем NULL и ordering semantics.

### `EXCEPT`

Для ``EXCEPT`` сначала определи grain/cardinality результата, затем NULL и ordering semantics.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Set operations: отдельный пример

```sql
SELECT email FROM newsletter_subscribers
UNION
SELECT email FROM registered_users

INTERSECT
SELECT email FROM verified_emails;
```

Set operations требуют совместимых columns; UNION удаляет duplicates, INTERSECT оставляет общие строки.

## Common mistakes

**Ошибка:** Использовать LIMIT без детерминированного ORDER BY или фильтровать правую таблицу LEFT JOIN в WHERE.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Set operations** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Предскажи cardinality результата и проверь, не размножает ли JOIN строки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT`.
- Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Использовать LIMIT без детерминированного ORDER BY или фильтровать правую таблицу LEFT JOIN в WHERE.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT`.

## Задача

Разбери backend-сценарий: **Предскажи cardinality результата и проверь, не размножает ли JOIN строки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Set operations**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
