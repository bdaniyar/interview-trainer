# Lazy loading

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- объяснить `implicit query` своими словами и связать с backend-сценарием;
- объяснить `session dependency` своими словами и связать с backend-сценарием;
- объяснить `async pitfalls.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

SQLAlchemy 2.x управляет SQL, identity map, unit of work и transaction lifecycle; Session не является простым соединением.

В теме **Lazy loading** важно уверенно объяснять следующие части:

### implicit query

Для `implicit query` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### session dependency

Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

### async pitfalls

Для `async pitfalls` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Lazy loading: отдельный пример

```text
Сценарий: Доступ к relationship запускает SQL в serializer.

Проверка:
Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Lazy loading** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши session scope, момент flush/commit и количество SQL-запросов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- implicit query
- session dependency
- async pitfalls.
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

- implicit query
- session dependency
- async pitfalls.

## Задача

Разбери backend-сценарий: **Опиши session scope, момент flush/commit и количество SQL-запросов.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Unexpected lazy load

**Сценарий:** Доступ к relationship запускает SQL в serializer.

**Rubric:** Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Detached instance

**Сценарий:** После закрытия Session serializer читает unloaded relationship и падает.

**Rubric:** Сформировать DTO внутри session boundary или eager-load нужное; не возвращать live ORM entity наружу.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Lazy loading**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
