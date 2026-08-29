# Add, flush, commit and refresh

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- объяснить ``add`` своими словами и связать с backend-сценарием;
- объяснить ``flush` sends SQL inside transaction` своими словами и связать с backend-сценарием;
- объяснить ``commit` finalizes` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

SQLAlchemy 2.x управляет SQL, identity map, unit of work и transaction lifecycle; Session не является простым соединением.

В теме **Add, flush, commit and refresh** важно уверенно объяснять следующие части:

### `add`

Для ``add`` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### `flush` sends SQL inside transaction

Flush синхронизирует pending ORM state с БД внутри текущей transaction и получает generated values, но не делает изменения durable как commit.

### `commit` finalizes

Для ``commit` finalizes` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### `refresh` reloads

Для ``refresh` reloads` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.

### generated ID may appear after flush

Flush синхронизирует pending ORM state с БД внутри текущей transaction и получает generated values, но не делает изменения durable как commit.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Add, flush, commit and refresh: отдельный пример

```text
Сценарий: repository.save неожиданно commit-ит половину use case.

Проверка:
Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Add, flush, commit and refresh** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши session scope, момент flush/commit и количество SQL-запросов. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads
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

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads
- generated ID may appear after flush.

## Задача

### Flush generated id

add_and_flush делает add+flush и возвращает entity; commit запрещён.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Debugging practice

### Commit in repository

**Сценарий:** repository.save неожиданно commit-ит половину use case.

**Rubric:** Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Add, flush, commit and refresh**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
