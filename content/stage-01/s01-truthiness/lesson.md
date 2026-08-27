# Truthiness

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `falsy values` своими словами и связать с backend-сценарием;
- объяснить ``bool`` своими словами и связать с backend-сценарием;
- объяснить ``__bool__`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.

В теме **Truthiness** важно уверенно объяснять следующие части:

### falsy values

Для `falsy values` проследи конкретный object, его type/identity и все bindings до и после операции.

### `bool`

Для ``bool`` проследи конкретный object, его type/identity и все bindings до и после операции.

### `__bool__`

Для ``__bool__`` проследи конкретный object, его type/identity и все bindings до и после операции.

### `__len__`

Для ``__len__`` проследи конкретный object, его type/identity и все bindings до и после операции.

### `if value` vs `if value is None`

Для ``if value` vs `if value is None`` проследи конкретный object, его type/identity и все bindings до и после операции.

### backend bugs with `0`, `""` and empty collections

Для `backend bugs with `0`, `""` and empty collections` проследи конкретный object, его type/identity и все bindings до и после операции.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
payload = {"roles": ["reader"]}
alias = payload
alias["roles"].append("writer")
assert payload["roles"] == ["reader", "writer"]
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Объяснять переменную как коробку, которая всегда содержит независимое значение.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Truthiness** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- falsy values
- `bool`
- `__bool__`
- `__len__`
- Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Объяснять переменную как коробку, которая всегда содержит независимое значение.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- falsy values
- `bool`
- `__bool__`
- `__len__`
- `if value` vs `if value is None`
- backend bugs with `0`, `""` and empty collections.

## Задача

### Не потерять нулевой limit

Верни default только для None. Целое значение от 0 до 100 сохрани; bool и остальные значения отклони через ValueError.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Truthiness пользовательского объекта

```python
class Queue:
    def __len__(self):
        return 0

print(bool(Queue()))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
False
```

Если __bool__ не определён, bool использует __len__; нулевая длина означает falsy.

Misconception: `truthiness`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Truthiness**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
