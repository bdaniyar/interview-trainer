# Response models

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- объяснить `contract` своими словами и связать с backend-сценарием;
- объяснить `serialization` своими словами и связать с backend-сценарием;
- объяснить `filtering fields` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.

В теме **Response models** важно уверенно объяснять следующие части:

### contract

Для `contract` проследи request через router, validation/dependencies, handler/service и response serialization.

### serialization

Для `serialization` проследи request через router, validation/dependencies, handler/service и response serialization.

### filtering fields

Для `filtering fields` проследи request через router, validation/dependencies, handler/service и response serialization.

### avoiding secret leakage

Для `avoiding secret leakage` проследи request через router, validation/dependencies, handler/service и response serialization.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Response models: отдельный пример

```text
Сценарий: Endpoint возвращает ORM object вместе с password_hash.

Проверка:
Явная response model/DTO с allowlist полей; contract test проверяет отсутствие secret.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Открывать Session глобально или выполнять blocking I/O в async route.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Response models** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи request от router через dependency и service до response model. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- contract
- serialization
- filtering fields
- avoiding secret leakage.
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

- contract
- serialization
- filtering fields
- avoiding secret leakage.

## Задача

### Не раскрыть secret

UserPublic response_model для GET /users/me должен удалить password_hash из handler result.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Debugging practice

### Secret ORM field

**Сценарий:** Endpoint возвращает ORM object вместе с password_hash.

**Rubric:** Явная response model/DTO с allowlist полей; contract test проверяет отсутствие secret.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Response models**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
