# BackgroundTasks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- объяснить `runs after response in same application process` своими словами и связать с backend-сценарием;
- объяснить `small non-critical work` своими словами и связать с backend-сценарием;
- объяснить `not durable` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.

В теме **BackgroundTasks** важно уверенно объяснять следующие части:

### runs after response in same application process

Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

### small non-critical work

Для `small non-critical work` проследи request через router, validation/dependencies, handler/service и response serialization.

### not durable

Для `not durable` проследи request через router, validation/dependencies, handler/service и response serialization.

### lost on crash

Для `lost on crash` проследи request через router, validation/dependencies, handler/service и response serialization.

### not a replacement for Celery/outbox

Для `not a replacement for Celery/outbox` проследи request через router, validation/dependencies, handler/service и response serialization.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### BackgroundTasks: отдельный пример

```python
def example_s14_backgroundtasks() -> tuple[str, ...]:
    # BackgroundTasks: проверяем отдельный contract урока.
    return ('runs after response in same application process', 'small non-critical work', 'not durable', 'lost on crash',)

assert example_s14_backgroundtasks()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

**Ошибка:** Открывать Session глобально или выполнять blocking I/O в async route.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **BackgroundTasks** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи request от router через dependency и service до response model. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- runs after response in same application process
- small non-critical work
- not durable
- lost on crash
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

- runs after response in same application process
- small non-critical work
- not durable
- lost on crash
- not a replacement for Celery/outbox.

## Задача

Разбери backend-сценарий: **Проследи request от router через dependency и service до response model.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **BackgroundTasks**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
