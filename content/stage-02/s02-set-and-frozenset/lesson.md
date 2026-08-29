# Set and frozenset

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Set and frozenset**, а не только запомнить термин;
- прочитать и изменить короткий пример для `uniqueness`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`set` is a mutable unordered collection of unique hashable elements; `frozenset` is its immutable hashable variant.

### Как работает

Membership, add and remove are average O(1) through hashing. Union `|`, intersection `&` and difference `-` express standard set operations.


### Важный нюанс / limitation

Set iteration order is not a business contract. Sorting is required when output order matters; converting to set also discards duplicates.

### Где используется в backend

Sets are useful for permission membership or deduplication when original order is not required.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- uniqueness
- membership
- union/intersection/difference
- deduplication

### Полезно

- set vs list
- frozenset

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Set and frozenset: отдельный пример

```python
requested = {"read", "write"}
granted = frozenset({"read", "moderate"})

print(requested & granted)
print(requested <= granted)
```

Set operations прямо выражают пересечение и проверку подмножества permissions.

## Common mistakes

### Ошибка 1

Returning `list(set(values))` from an API silently loses deterministic ordering.

## Practice

**A · Code/result prediction.** Change one input in the `uniqueness` example and predict the result before running it.

**B · Find the bug.** Find code that violates `membership` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `uniqueness` and add one edge-case test.

**E · Interview explanation.** Explain Set and frozenset in 45–60 seconds and include one limitation.

## Code prediction

### set удаляет дубликаты

```python
values = {3, 1, 3, 2}
print(len(values), sorted(values))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
3 [1, 2, 3]
```

set хранит уникальные hashable значения; порядок вывода делают явным через sorted.

Misconception: `set-order`.

</details>

## Interview questions

### Основной вопрос

Что такое Set and frozenset и как это работает?

### Follow-up

Какая типичная ошибка связана с Set and frozenset?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`set` is a mutable unordered collection of unique hashable elements; `frozenset` is its immutable hashable variant.

### Нормальный Junior answer

> `set` is a mutable unordered collection of unique hashable elements; `frozenset` is its immutable hashable variant. Membership, add and remove are average O(1) through hashing. Union `|`, intersection `&` and difference `-` express standard set operations. Важное ограничение: Set iteration order is not a business contract. Sorting is required when output order matters; converting to set also discards duplicates.

### Углубление / follow-up

**Какая типичная ошибка связана с Set and frozenset?**

Returning `list(set(values))` from an API silently loses deterministic ordering.

## Expected answer rubric

### Must mention

- uniqueness
- membership
- union/intersection/difference
- deduplication

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning `list(set(values))` from an API silently loses deterministic ordering.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Set and frozenset?

## Задача

### Нормализовать scopes

Верни frozenset непустых scopes в lower-case без пробелов и дублей.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `set` is a mutable unordered collection of unique hashable elements; `frozenset` is its immutable hashable variant.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** Returning `list(set(values))` from an API silently loses deterministic ordering.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
