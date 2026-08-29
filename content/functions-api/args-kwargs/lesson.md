# `*args`, `**kwargs` and unpacking

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `collection` своими словами и связать с backend-сценарием;
- объяснить `forwarding` своими словами и связать с backend-сценарием;
- объяснить `iterable/dict unpacking` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **`*args`, `**kwargs` and unpacking** важно уверенно объяснять следующие части:

### collection

Для `collection` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### forwarding

Для `forwarding` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### iterable/dict unpacking

`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

### duplicate arguments

Для `duplicate arguments` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### wrapper functions

Для `wrapper functions` отдели definition time от call time и покажи влияние на signature, scope или state функции.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### `*args`, `**kwargs` and unpacking: отдельный пример

```python
def audit(event, *entity_ids, request_id=None, **details):
    return event, entity_ids, request_id, details

context = {"request_id": "req-7", "actor": 42}
print(audit("updated", 10, 11, **context))
```

`*args` собирает positional IDs, `**kwargs` — дополнительные named fields; unpacking разворачивает mapping при вызове.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **`*args`, `**kwargs` and unpacking** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- collection
- forwarding
- iterable/dict unpacking
- duplicate arguments
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

- collection
- forwarding
- iterable/dict unpacking
- duplicate arguments
- wrapper functions.

## Задача

### Объединить options

Объедини base и keyword overrides, где overrides побеждают. Не изменяй входной dict.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`*args`, `**kwargs` and unpacking**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
