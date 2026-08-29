# Safe schema changes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- объяснить `expand/contract` своими словами и связать с backend-сценарием;
- объяснить `nullable → backfill → constraint` своими словами и связать с backend-сценарием;
- объяснить `indexes on large tables` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Alembic хранит версионированную историю изменений схемы; autogenerate создаёт кандидат на migration, а не доказательство корректности.

В теме **Safe schema changes** важно уверенно объяснять следующие части:

### expand/contract

Для `expand/contract` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

### nullable → backfill → constraint

Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

### indexes on large tables

Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

### backward compatibility

Для `backward compatibility` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Safe schema changes: отдельный пример

```bash
alembic revision -m "s17_safe_schema_changes"
# review upgrade/downgrade for: expand/contract, nullable → backfill → constraint, indexes on large tables, backward compatibility
alembic upgrade head
```

Review migration как versioned schema transition; autogenerate — только кандидат.

## Common mistakes

**Ошибка:** Слепо принимать autogenerate или совмещать несовместимое изменение в один deploy.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Safe schema changes** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Предложи expand/contract sequence для изменения schema без остановки API. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- expand/contract
- nullable → backfill → constraint
- indexes on large tables
- backward compatibility.
- Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Слепо принимать autogenerate или совмещать несовместимое изменение в один deploy.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- expand/contract
- nullable → backfill → constraint
- indexes on large tables
- backward compatibility.

## Задача

Разбери backend-сценарий: **Предложи expand/contract sequence для изменения schema без остановки API.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Safe schema changes**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
