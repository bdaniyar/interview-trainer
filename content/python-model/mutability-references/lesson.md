# Mutability and immutability

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `mutable/immutable` своими словами и связать с backend-сценарием;
- объяснить `mutation vs rebinding` своими словами и связать с backend-сценарием;
- объяснить `list, dict, set` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Переменные в Python — имена, связанные с объектами. Если два имени ссылаются на изменяемый объект, мутация наблюдается через обе ссылки.

```python
original = {"roles": ["reader"]}
alias = original
alias["roles"].append("writer")
assert original["roles"] == ["reader", "writer"]
```

Переприсваивание имени не меняет прежний объект, а связывает имя с новым. Мутация, напротив, сохраняет identity объекта.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Mutability and immutability: отдельный пример

```python
roles = ["reader"]
original_id = id(roles)
roles.append("writer")

name = "api"
old_name_id = id(name)
name += "-v2"

print(id(roles) == original_id)
print(id(name) == old_name_id)
```

List меняется с сохранением identity; операция со строкой создаёт новый immutable объект.

## Common mistakes

**Ошибка:** Объяснять переменную как коробку, которая всегда содержит независимое значение.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Mutability and immutability** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- mutable/immutable
- mutation vs rebinding
- list, dict, set
- int, str, bytes, tuple
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

- mutable/immutable
- mutation vs rebinding
- list, dict, set
- int, str, bytes, tuple
- tuple с mutable element
- effect on function arguments.

## Задача

Реализуй `append_marker(items, marker)`: добавь marker в переданный список и верни **тот же** список. Не создавай копию.

## Code prediction

### Два имени одного списка

```python
a = []
b = a
b.append(1)
print(a)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1]
```

Assignment связал b с тем же mutable list; append виден через оба имени.

Misconception: `aliasing`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Mutability and immutability**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
