# Union, Optional and `|`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- объяснить `optional value` своими словами и связать с backend-сценарием;
- объяснить `required nullable field distinction` своими словами и связать с backend-сценарием;
- объяснить `narrowing.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Type hints улучшают статический анализ и контракты, но сами по себе не валидируют runtime-данные.

В теме **Union, Optional and `|`** важно уверенно объяснять следующие части:

### optional value

`T | None` разрешает значение `None`, но не делает аргумент или поле необязательным без default; missing и explicit null — разные состояния.

### required nullable field distinction

`NULL` означает отсутствие известного значения; сравнение с ним делают через `IS NULL`, а многие выражения дают `UNKNOWN`.

### narrowing

Для `narrowing` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Union, Optional and `|`: отдельный пример

```python
def normalize(value: str | None) -> str:
    return value.strip() if value is not None else ""

print(normalize(None))
try:
    normalize()
except TypeError:
    print("argument is still required")
```

Nullable type разрешает `None`, но отсутствие default не делает argument optional при вызове.

## Common mistakes

**Ошибка:** Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Union, Optional and `|`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- optional value
- required nullable field distinction
- narrowing.
- Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- optional value
- required nullable field distinction
- narrowing.

## Задача

Разбери backend-сценарий: **Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Optional не создаёт default

```python
def parse(value: str | None):
    return value is None
try:
    parse()
except TypeError:
    print('missing')
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
missing
```

Union с None разрешает значение None, но параметр остаётся обязательным без default.

Misconception: `optional-vs-default`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Union, Optional and `|`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
