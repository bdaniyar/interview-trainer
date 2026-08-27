# Revision, upgrade and downgrade

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- объяснить `Revision, upgrade and downgrade` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Alembic хранит версионированную историю изменений схемы; autogenerate создаёт кандидат на migration, а не доказательство корректности.

В теме **Revision, upgrade and downgrade** важно уверенно объяснять следующие части:

### Revision, upgrade and downgrade

Для `Revision, upgrade and downgrade` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```bash
alembic revision --autogenerate -m "add booking status"
alembic upgrade head
alembic current
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Слепо принимать autogenerate или совмещать несовместимое изменение в один deploy.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Revision, upgrade and downgrade** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Предложи expand/contract sequence для изменения schema без остановки API. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- Revision, upgrade and downgrade
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

- Revision, upgrade and downgrade

## Задача

Разбери backend-сценарий: **Предложи expand/contract sequence для изменения schema без остановки API.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Revision, upgrade and downgrade**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
