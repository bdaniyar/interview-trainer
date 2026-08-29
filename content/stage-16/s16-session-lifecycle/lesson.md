# Session lifecycle

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- объяснить `create` своими словами и связать с backend-сценарием;
- объяснить `use` своими словами и связать с backend-сценарием;
- объяснить `commit/rollback` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

SQLAlchemy 2.x управляет SQL, identity map, unit of work и transaction lifecycle; Session не является простым соединением.

В теме **Session lifecycle** важно уверенно объяснять следующие части:

### create

Для `create` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### use

Для `use` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### commit/rollback

Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя.

### close

Для `close` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### request-scoped session

LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`.

### never share one session globally

Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Session lifecycle: отдельный пример

```python
def example_s16_session_lifecycle() -> tuple[str, ...]:
    # Session lifecycle: проверяем отдельный contract урока.
    return ('create', 'use', 'commit/rollback', 'close',)

assert example_s16_session_lifecycle()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Common mistakes

**Ошибка:** Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Session lifecycle** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши session scope, момент flush/commit и количество SQL-запросов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- create
- use
- commit/rollback
- close
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

- create
- use
- commit/rollback
- close
- request-scoped session
- never share one session globally.

## Задача

Разбери backend-сценарий: **Опиши session scope, момент flush/commit и количество SQL-запросов.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Session lifecycle**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
