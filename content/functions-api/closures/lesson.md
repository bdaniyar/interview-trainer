# Closures and free variables

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `closure` своими словами и связать с backend-сценарием;
- объяснить `enclosing scope` своими словами и связать с backend-сценарием;
- объяснить `free variable` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **Closures and free variables** важно уверенно объяснять следующие части:

### closure

Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

### enclosing scope

LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`.

### free variable

Для `free variable` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### retained state

Для `retained state` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### practical factory/callback examples

Для `practical factory/callback examples` отдели definition time от call time и покажи влияние на signature, scope или state функции.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Closures and free variables: отдельный пример

```python
def make_prefixer(prefix):
    def render(value):
        return f"{prefix}:{value}"
    return render

user_key = make_prefixer("user")
print(user_key(42))
```

Closure продолжает видеть binding `prefix` после завершения внешней функции.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Closures and free variables** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- closure
- enclosing scope
- free variable
- retained state
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

- closure
- enclosing scope
- free variable
- retained state
- practical factory/callback examples.

## Задача

### Stateful closure

Верни next_value closure: начальное состояние start; каждый вызов увеличивает его на step и возвращает новое значение.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Closure хранит binding

```python
def make(prefix):
    def render(value):
        return f'{prefix}:{value}'
    return render
print(make('id')(7))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
id:7
```

Внутренняя функция замыкает свободное имя prefix после завершения make.

Misconception: `closure`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Closures and free variables**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
