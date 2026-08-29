# Late binding

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `closures inside loop` своими словами и связать с backend-сценарием;
- объяснить `lambdas` своими словами и связать с backend-сценарием;
- объяснить `lookup at call time` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **Late binding** важно уверенно объяснять следующие части:

### closures inside loop

Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

### lambdas

Для `lambdas` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### lookup at call time

Для `lookup at call time` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### fix through default argument

Для `fix through default argument` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### factory function

Для `factory function` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### `functools.partial`

Для ``functools.partial`` отдели definition time от call time и покажи влияние на signature, scope или state функции.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Late binding: отдельный пример

```python
bad = [lambda: value for value in range(3)]
good = [lambda value=value: value for value in range(3)]

print([fn() for fn in bad])
print([fn() for fn in good])
```

Late binding разрешает free variable при вызове; default argument фиксирует значение при создании lambda.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Late binding** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- closures inside loop
- lambdas
- lookup at call time
- fix through default argument
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

- closures inside loop
- lambdas
- lookup at call time
- fix through default argument
- factory function
- `functools.partial`.

## Задача

### Исправить late binding

Верни функции, каждая умножает аргумент на собственный multiplier из входа.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Late binding в цикле

```python
funcs = [lambda: i for i in range(3)]
print([fn() for fn in funcs])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[2, 2, 2]
```

Свободное имя i разрешается при вызове; после цикла оно равно 2.

Misconception: `late-binding`.

</details>

## Debugging practice

### Late closure

**Сценарий:** Callbacks из цикла используют последнее id.

**Rubric:** Free name resolved at call time; bind default/factory.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Late binding**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
