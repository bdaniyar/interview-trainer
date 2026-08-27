# Assignment, aliases and nested mutation

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `aliases` своими словами и связать с backend-сценарием;
- объяснить `shared nested structures` своими словами и связать с backend-сценарием;
- объяснить `repeated references` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.

В теме **Assignment, aliases and nested mutation** важно уверенно объяснять следующие части:

### aliases

Для `aliases` проследи конкретный object, его type/identity и все bindings до и после операции.

### shared nested structures

Для `shared nested structures` проследи конкретный object, его type/identity и все bindings до и после операции.

### repeated references

Для `repeated references` проследи конкретный object, его type/identity и все bindings до и после операции.

### `[[]] * 3`

Для ``[[]] * 3`` проследи конкретный object, его type/identity и все bindings до и после операции.

### passing objects into functions

Для `passing objects into functions` проследи конкретный object, его type/identity и все bindings до и после операции.

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

1. Объясни **Assignment, aliases and nested mutation** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- aliases
- shared nested structures
- repeated references
- `[[]] * 3`
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

- aliases
- shared nested structures
- repeated references
- `[[]] * 3`
- passing objects into functions.

## Задача

Разбери backend-сценарий: **Проследи identity и состояние объекта после двух присваиваний и одной мутации.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Повтор вложенного списка

```python
rows = [[0]] * 3
rows[0].append(1)
print(rows)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[[0, 1], [0, 1], [0, 1]]
```

Оператор * повторил одну ссылку на внутренний список, а не создал три списка.

Misconception: `nested-aliasing`.

</details>

## Debugging practice

### Nested alias

**Сценарий:** [[]] * 3 меняет все строки после append.

**Rubric:** Повторяется одна reference; comprehension создаёт независимые lists.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Assignment, aliases and nested mutation**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
