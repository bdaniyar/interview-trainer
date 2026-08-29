# Lifespan

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- объяснить `startup/shutdown` своими словами и связать с backend-сценарием;
- объяснить `shared client/pool initialization` своими словами и связать с backend-сценарием;
- объяснить `cleanup` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.

В теме **Lifespan** важно уверенно объяснять следующие части:

### startup/shutdown

Для `startup/shutdown` проследи request через router, validation/dependencies, handler/service и response serialization.

### shared client/pool initialization

Для `shared client/pool initialization` проследи request через router, validation/dependencies, handler/service и response serialization.

### cleanup

Для `cleanup` проследи request через router, validation/dependencies, handler/service и response serialization.

### modern lifespan over scattered legacy hooks

Lifespan управляет ресурсами уровня приложения: код до `yield` создаёт client/pool, код после `yield` гарантированно закрывает их при shutdown.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Lifespan: отдельный пример

```text
Сценарий: HTTP client создаётся на startup, но socket остаётся после shutdown.

Проверка:
Lifespan async context manager с cleanup в finally; test lifespan and close state.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Открывать Session глобально или выполнять blocking I/O в async route.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Lifespan** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи request от router через dependency и service до response model. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- startup/shutdown
- shared client/pool initialization
- cleanup
- modern lifespan over scattered legacy hooks.
- Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Открывать Session глобально или выполнять blocking I/O в async route.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- startup/shutdown
- shared client/pool initialization
- cleanup
- modern lifespan over scattered legacy hooks.

## Задача

Разбери backend-сценарий: **Проследи request от router через dependency и service до response model.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Resource not closed

**Сценарий:** HTTP client создаётся на startup, но socket остаётся после shutdown.

**Rubric:** Lifespan async context manager с cleanup в finally; test lifespan and close state.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Lifespan**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
