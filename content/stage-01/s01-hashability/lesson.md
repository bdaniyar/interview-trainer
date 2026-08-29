# Hashability

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `hashable object` своими словами и связать с backend-сценарием;
- объяснить `dict key/set member` своими словами и связать с backend-сценарием;
- объяснить `equality/hash contract` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.

В теме **Hashability** важно уверенно объяснять следующие части:

### hashable object

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

### dict key/set member

`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

### equality/hash contract

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

### mutable object as key

Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

### tuple hashability

`tuple` — immutable sequence; hashability зависит от всех элементов, а неизменяемость контейнера не делает mutable элементы неизменяемыми.

### custom `__hash__`

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Hashability: отдельный пример

```python
keys = {(1, 2): "point"}
print(keys[(1, 2)])

try:
    {[1, 2]: "broken"}
except TypeError as exc:
    print(type(exc).__name__)
```

Tuple из hashable элементов допустим как ключ, mutable list — нет.

## Common mistakes

**Ошибка:** Объяснять переменную как коробку, которая всегда содержит независимое значение.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Hashability** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- hashable object
- dict key/set member
- equality/hash contract
- mutable object as key
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

- hashable object
- dict key/set member
- equality/hash contract
- mutable object as key
- tuple hashability
- custom `__hash__`.

## Задача

Разбери backend-сценарий: **Проследи identity и состояние объекта после двух присваиваний и одной мутации.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Равные ключи dict

```python
data = {True: 'yes', 1: 'one'}
print(len(data), data[True])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
1 one
```

True == 1 и их hashes равны, поэтому второй assignment заменяет значение того же ключа.

Misconception: `hash-equality-contract`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Hashability**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
