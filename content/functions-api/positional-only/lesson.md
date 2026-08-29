# Positional-only and keyword-only parameters

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить ``/`` своими словами и связать с backend-сценарием;
- объяснить ``*`` своими словами и связать с backend-сценарием;
- объяснить `API design` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **Positional-only and keyword-only parameters** важно уверенно объяснять следующие части:

### `/`

Для ``/`` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### `*`

Для ``*`` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### API design

Для `API design` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### readable signatures

Signature — публичный контракт вызова: kinds параметров, defaults и annotations определяют допустимые positional/keyword arguments и помогают introspection.

### backward compatibility

Для `backward compatibility` отдели definition time от call time и покажи влияние на signature, scope или state функции.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Positional-only and keyword-only parameters: отдельный пример

```python
def paginate(resource, /, *, limit=20, offset=0):
    return resource[offset : offset + limit]

print(paginate([1, 2, 3], limit=2))
```

`resource` скрывает имя positional-only параметра, а параметры pagination требуют явных keywords.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Positional-only and keyword-only parameters** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `/`
- `*`
- API design
- readable signatures
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

- `/`
- `*`
- API design
- readable signatures
- backward compatibility.

## Задача

### Явная сигнатура pagination helper

Реализуй build_page_query: resource positional-only; limit и offset keyword-only. Проверь resource, limit 1..100 и offset >= 0.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Keyword-only argument

```python
def page(limit, *, offset=0):
    return limit, offset
print(page(10, offset=20))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
(10, 20)
```

Параметр после * можно передать только по имени, что делает API вызова явным.

Misconception: `keyword-only`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Positional-only and keyword-only parameters**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
