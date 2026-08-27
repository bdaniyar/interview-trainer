# Default arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- объяснить `evaluation at function definition` своими словами и связать с backend-сценарием;
- объяснить `mutable default bug` своими словами и связать с backend-сценарием;
- объяснить `sentinel pattern` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Значения параметров по умолчанию вычисляются один раз — при выполнении `def`. Поэтому список в сигнатуре сохраняется между вызовами.

```python
def broken(value, bucket=[]):
    bucket.append(value)
    return bucket
```

Используй `None` как sentinel и создавай новый список внутри вызова.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
def list_users(limit: int = 20, *, active: bool | None = None) -> list[dict]:
    """Явный API: active нельзя передать случайно позиционно."""
    return []
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Default arguments** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- evaluation at function definition
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations.
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

- evaluation at function definition
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations.

## Задача

Реализуй `add_tag(tag, tags=None)`. Функция возвращает список с добавленным тегом. Вызовы без `tags` не должны делить состояние; переданный список нужно изменить на месте.

## Code prediction

### Default вычисляется один раз

```python
def add(value, bucket=[]):
    bucket.append(value)
    return bucket

print(add(1), add(2))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1] [1, 2]
```

Mutable default создаётся при выполнении def и переиспользуется следующими вызовами.

Misconception: `mutable-default`.

</details>

## Debugging practice

### Mutable default

**Сценарий:** Список tags растёт между независимыми вызовами.

**Rubric:** Default создаётся при def; None/sentinel и новый list; тест на два вызова.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Default arguments**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
