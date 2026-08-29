# Truthiness

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Truthiness**, а не только запомнить термин;
- прочитать и изменить короткий пример для `falsy values`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Truthiness is Python's protocol for converting an object to boolean context such as `if value`.

### Как работает

Python calls `__bool__`; if absent, it uses `__len__`; without both, an object is truthy. `None`, numeric zero and empty standard collections are falsy.


### Важный нюанс / limitation

`if value` merges several states. Use `is None` when zero, empty string or empty list is valid data rather than absence.

### Где используется в backend

Pagination offset `0` and an empty JSON array may be valid values and must not be confused with missing input.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- falsy values
- `bool`
- `__bool__`
- `__len__`

### Полезно

- `if value` vs `if value is None`
- backend bugs with `0`, `""` and empty collections

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Truthiness: отдельный пример

```python
class Queue:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

print(bool(Queue([])))
print(bool(Queue(["job"])))
```

При отсутствии `__bool__` Python использует `__len__`: ноль означает falsy.

## Common mistakes

### Ошибка 1

Replacing `if limit is None` with `if not limit` incorrectly rejects a valid zero when the contract permits it.

## Practice

**A · Code/result prediction.** Change one input in the `falsy values` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``bool`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `falsy values` and add one edge-case test.

**E · Interview explanation.** Explain Truthiness in 45–60 seconds and include one limitation.

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

## Interview questions

### Основной вопрос

Что такое Truthiness и как это работает?

### Follow-up

Какая типичная ошибка связана с Truthiness?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Truthiness is Python's protocol for converting an object to boolean context such as `if value`.

### Нормальный Junior answer

> Truthiness is Python's protocol for converting an object to boolean context such as `if value`. Python calls `__bool__`; if absent, it uses `__len__`; without both, an object is truthy. `None`, numeric zero and empty standard collections are falsy. Важное ограничение: `if value` merges several states. Use `is None` when zero, empty string or empty list is valid data rather than absence.

### Углубление / follow-up

**Какая типичная ошибка связана с Truthiness?**

Replacing `if limit is None` with `if not limit` incorrectly rejects a valid zero when the contract permits it.

## Expected answer rubric

### Must mention

- falsy values
- `bool`
- `__bool__`
- `__len__`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Replacing `if limit is None` with `if not limit` incorrectly rejects a valid zero when the contract permits it.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Truthiness?

## Задача

### Не потерять нулевой limit

Верни default только для None. Целое значение от 0 до 100 сохрани; bool и остальные значения отклони через ValueError.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Truthiness is Python's protocol for converting an object to boolean context such as `if value`.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Replacing `if limit is None` with `if not limit` incorrectly rejects a valid zero when the contract permits it.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
