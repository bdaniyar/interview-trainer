# Decorator factory and decorator arguments

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `three levels of functions` своими словами и связать с backend-сценарием;
- объяснить `configuration captured by closure` своими словами и связать с backend-сценарием;
- объяснить `retry/timing/permission examples.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **Decorator factory and decorator arguments** важно уверенно объяснять следующие части:

### three levels of functions

Для `three levels of functions` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### configuration captured by closure

Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

### retry/timing/permission examples

Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
def list_users(limit: int = 20, *, active: bool | None = None) -> list[dict]:
    """Явный API: active нельзя передать случайно позиционно."""
    return []
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Decorator factory and decorator arguments** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- three levels of functions
- configuration captured by closure
- retry/timing/permission examples.
- Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- three levels of functions
- configuration captured by closure
- retry/timing/permission examples.

## Задача

### Retry decorator

Реализуй retry(attempts, exceptions, on_retry). Повторяй только указанные errors, вызови hook перед retry и подними последнюю ошибку.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Decorator factory and decorator arguments**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
