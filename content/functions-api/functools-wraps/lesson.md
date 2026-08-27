# `functools.wraps`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `preserving `__name__`` своими словами и связать с backend-сценарием;
- объяснить `docstring` своими словами и связать с backend-сценарием;
- объяснить `annotations` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **`functools.wraps`** важно уверенно объяснять следующие части:

### preserving `__name__`

Для `preserving `__name__`` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### docstring

Для `docstring` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### annotations

Для `annotations` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### `__wrapped__`

Для ``__wrapped__`` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### why frameworks/tools care

Для `why frameworks/tools care` отдели definition time от call time и покажи влияние на signature, scope или state функции.

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

1. Объясни **`functools.wraps`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`
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

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`
- why frameworks/tools care.

## Задача

### Сохранить metadata wrapper

Реализуй traced decorator через functools.wraps и добавь wrapper.traced = True.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Decorator меняет вызываемый объект

```python
def twice(fn):
    def wrapper():
        return fn() * 2
    return wrapper

@twice
def answer():
    return 21
print(answer())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
42
```

После декорирования имя answer связано с wrapper, который вызывает исходную функцию.

Misconception: `decorator`.

</details>

## Debugging practice

### Missing wraps

**Сценарий:** FastAPI/introspection видит wrapper signature.

**Rubric:** functools.wraps сохраняет metadata и __wrapped__.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`functools.wraps`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
