# Identity and equality

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить ``id()`` своими словами и связать с backend-сценарием;
- объяснить ``is`` своими словами и связать с backend-сценарием;
- объяснить ``==`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

`is` отвечает на вопрос «это один и тот же объект?», а `==` — «считаются ли значения равными?». Эти операции нельзя взаимозаменять.

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)  # True
print(a is b)  # False
print(a is c)  # True
```

### Почему `is None` — правильно

`None` — singleton: в процессе существует один объект `None`. Проверка идентичности не вызывает пользовательский `__eq__` и точно выражает намерение.

> [!WARNING]
> Не полагайся на интернирование строк и малых целых: это деталь реализации, а не контракт задачи.

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

1. Объясни **Identity and equality** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `id()`
- `is`
- `==`
- identity vs value equality
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

- `id()`
- `is`
- `==`
- identity vs value equality
- `is None`
- почему нельзя полагаться на interning
- custom `__eq__`.

## Задача

Реализуй `compare_objects(left, right)`, которая возвращает словарь с ключами `same_identity` и `same_value`.

## Code prediction

### Identity не равна equality

```python
a = [1]
b = [1]
print(a == b, a is b)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
True False
```

Списки равны по содержимому, но созданы как два разных объекта.

Misconception: `identity-vs-equality`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Identity and equality**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
