# Numbers, strings, bytes and encoding

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `int/float/Decimal basics` своими словами и связать с backend-сценарием;
- объяснить `floating-point precision` своими словами и связать с backend-сценарием;
- объяснить ``str` vs `bytes`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.

В теме **Numbers, strings, bytes and encoding** важно уверенно объяснять следующие части:

### int/float/Decimal basics

Для `int/float/Decimal basics` проследи конкретный object, его type/identity и все bindings до и после операции.

### floating-point precision

Для `floating-point precision` проследи конкретный object, его type/identity и все bindings до и после операции.

### `str` vs `bytes`

Для ``str` vs `bytes`` проследи конкретный object, его type/identity и все bindings до и после операции.

### Unicode

Для `Unicode` проследи конкретный object, его type/identity и все bindings до и после операции.

### encode/decode

Для `encode/decode` проследи конкретный object, его type/identity и все bindings до и после операции.

### JSON/text boundaries

Для `JSON/text boundaries` проследи конкретный object, его type/identity и все bindings до и после операции.

### money should not use binary float blindly

Для `money should not use binary float blindly` проследи конкретный object, его type/identity и все bindings до и после операции.

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

1. Объясни **Numbers, strings, bytes and encoding** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- int/float/Decimal basics
- floating-point precision
- `str` vs `bytes`
- Unicode
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

- int/float/Decimal basics
- floating-point precision
- `str` vs `bytes`
- Unicode
- encode/decode
- JSON/text boundaries
- money should not use binary float blindly.

## Задача

Разбери backend-сценарий: **Проследи identity и состояние объекта после двух присваиваний и одной мутации.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Numbers, strings, bytes and encoding**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
