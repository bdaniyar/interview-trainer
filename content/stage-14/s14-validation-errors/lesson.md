# Validation errors

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- объяснить `request validation` своими словами и связать с backend-сценарием;
- объяснить `422 convention` своими словами и связать с backend-сценарием;
- объяснить `custom validation response only with reason.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.

В теме **Validation errors** важно уверенно объяснять следующие части:

### request validation

Для `request validation` проследи request через router, validation/dependencies, handler/service и response serialization.

### 422 convention

Для `422 convention` проследи request через router, validation/dependencies, handler/service и response serialization.

### custom validation response only with reason

Для `custom validation response only with reason` проследи request через router, validation/dependencies, handler/service и response serialization.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Validation errors: отдельный пример

```python
def example_s14_validation_errors() -> tuple[str, ...]:
    # Validation errors: проверяем отдельный contract урока.
    return ('request validation', '422 convention', 'custom validation response only with reason',)

assert example_s14_validation_errors()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

**Ошибка:** Открывать Session глобально или выполнять blocking I/O в async route.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Validation errors** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи request от router через dependency и service до response model. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- request validation
- 422 convention
- custom validation response only with reason.
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

- request validation
- 422 convention
- custom validation response only with reason.

## Задача

Разбери backend-сценарий: **Проследи request от router через dependency и service до response model.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Validation errors**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
