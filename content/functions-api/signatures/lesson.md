# Parameters vs arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `parameter` своими словами и связать с backend-сценарием;
- объяснить `argument` своими словами и связать с backend-сценарием;
- объяснить `positional` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.

В теме **Parameters vs arguments** важно уверенно объяснять следующие части:

### parameter

Для `parameter` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### argument

Для `argument` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### positional

Для `positional` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### keyword

Для `keyword` отдели definition time от call time и покажи влияние на signature, scope или state функции.

### binding process

Binding — связь имени с объектом в namespace; assignment меняет связь имени, а mutation меняет состояние уже связанного объекта.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Parameters vs arguments: отдельный пример

```python
def create_user(email, active=True):
    return {"email": email, "active": active}

user = create_user("a@example.com", active=False)
print(user)
```

`email` и `active` — parameters определения; переданные значения — arguments конкретного вызова.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Parameters vs arguments** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- parameter
- argument
- positional
- keyword
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

- parameter
- argument
- positional
- keyword
- binding process.

## Задача

Разбери backend-сценарий: **Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Parameters vs arguments**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
