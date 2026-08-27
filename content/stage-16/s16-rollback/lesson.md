# Rollback

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- объяснить `failed transaction state` своими словами и связать с backend-сценарием;
- объяснить `rollback before reuse` своими словами и связать с backend-сценарием;
- объяснить `exception boundary.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

SQLAlchemy 2.x управляет SQL, identity map, unit of work и transaction lifecycle; Session не является простым соединением.

В теме **Rollback** важно уверенно объяснять следующие части:

### failed transaction state

Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

### rollback before reuse

Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя.

### exception boundary

Для `exception boundary` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

statement = (
    select(User)
    .options(selectinload(User.roles))
    .where(User.active.is_(True))
)
users = session.scalars(statement).all()
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Rollback** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши session scope, момент flush/commit и количество SQL-запросов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- failed transaction state
- rollback before reuse
- exception boundary.
- Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- failed transaction state
- rollback before reuse
- exception boundary.

## Задача

### Rollback failed unit of work

persist делает add+commit; на любой Exception rollback и re-raise.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Debugging practice

### Failed session

**Сценарий:** После IntegrityError новые queries падают.

**Rubric:** Rollback failed transaction before reuse.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Rollback**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
