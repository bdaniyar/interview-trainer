# Shallow and deep copy

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `slicing` своими словами и связать с backend-сценарием;
- объяснить ``list.copy`` своими словами и связать с backend-сценарием;
- объяснить ``dict.copy`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.

В теме **Shallow and deep copy** важно уверенно объяснять следующие части:

### slicing

Для `slicing` проследи конкретный object, его type/identity и все bindings до и после операции.

### `list.copy`

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### `dict.copy`

`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

### `copy.copy`

Для ``copy.copy`` проследи конкретный object, его type/identity и все bindings до и после операции.

### `copy.deepcopy`

Для ``copy.deepcopy`` проследи конкретный object, его type/identity и все bindings до и после операции.

### nested mutable data

Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

### when deepcopy is inappropriate

Для `when deepcopy is inappropriate` проследи конкретный object, его type/identity и все bindings до и после операции.

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

1. Объясни **Shallow and deep copy** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- slicing
- `list.copy`
- `dict.copy`
- `copy.copy`
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

- slicing
- `list.copy`
- `dict.copy`
- `copy.copy`
- `copy.deepcopy`
- nested mutable data
- when deepcopy is inappropriate.

## Задача

### Изолировать вложенный payload

Верни независимую глубокую копию payload. Мутация вложенных list/dict результата не должна менять оригинал.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Shallow copy

```python
source = {'roles': ['reader']}
copy = source.copy()
copy['roles'].append('writer')
print(source['roles'])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
['reader', 'writer']
```

Копия отделила внешний dict, но вложенный list остался общим.

Misconception: `shallow-copy`.

</details>

## Debugging practice

### Shallow copy

**Сценарий:** dict.copy не изолировал nested roles.

**Rubric:** Outer container новый, nested object общий; selective/deep copy по ownership.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Shallow and deep copy**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
