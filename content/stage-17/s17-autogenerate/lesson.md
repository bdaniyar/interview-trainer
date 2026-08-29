# Autogenerate

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- объяснить `generated diff is a draft` своими словами и связать с backend-сценарием;
- объяснить `manual review` своими словами и связать с backend-сценарием;
- объяснить `rename may look like drop/add.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Alembic хранит версионированную историю изменений схемы; autogenerate создаёт кандидат на migration, а не доказательство корректности.

В теме **Autogenerate** важно уверенно объяснять следующие части:

### generated diff is a draft

Для `generated diff is a draft` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

### manual review

Для `manual review` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

### rename may look like drop/add

Для `rename may look like drop/add` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Autogenerate: отдельный пример

```python
def unsafe_operations(operations):
    raise NotImplementedError
```

Это публичный starter contract практики «Review autogenerate». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

**Ошибка:** Слепо принимать autogenerate или совмещать несовместимое изменение в один deploy.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Autogenerate** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Предложи expand/contract sequence для изменения schema без остановки API. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- generated diff is a draft
- manual review
- rename may look like drop/add.
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

- generated diff is a draft
- manual review
- rename may look like drop/add.

## Задача

### Review autogenerate

unsafe_operations возвращает DROP/DELETE/SET NOT NULL/nullable=false operations без изменения порядка.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Autogenerate**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
