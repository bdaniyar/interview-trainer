# Comprehensions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Comprehensions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `list/dict/set comprehensions`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A comprehension builds a list, dict or set from an expression, source iterable and optional filters; a generator expression stays lazy.

### Как работает

The expression runs once per selected input item. Comprehension loop variables have their own scope in Python 3, while referenced outer names are read normally.


### Важный нюанс / limitation

Prefer a regular loop when there are several branches, side effects or nested transformations that hide intent.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- list/dict/set comprehensions
- generator expressions
- nested comprehensions
- scope

### Полезно

- readability
- when a regular loop is better

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Comprehensions: отдельный пример

```python
rows = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
]
active_ids = [row["id"] for row in rows if row["active"]]

print(active_ids)
```

Comprehension объединяет преобразование и короткий filter без скрытых side effects.

## Common mistakes

### Ошибка 1

A dense nested comprehension can be syntactically valid but harder to review and debug than a four-line loop.

## Practice

**A · Code/result prediction.** Change one input in the `list/dict/set comprehensions` example and predict the result before running it.

**B · Find the bug.** Find code that violates `generator expressions` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `list/dict/set comprehensions` and add one edge-case test.

**E · Interview explanation.** Explain Comprehensions in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Comprehensions и как это работает?

### Follow-up

Какая типичная ошибка связана с Comprehensions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A comprehension builds a list, dict or set from an expression, source iterable and optional filters; a generator expression stays lazy.

### Нормальный Junior answer

> A comprehension builds a list, dict or set from an expression, source iterable and optional filters; a generator expression stays lazy. The expression runs once per selected input item. Comprehension loop variables have their own scope in Python 3, while referenced outer names are read normally. Важное ограничение: Prefer a regular loop when there are several branches, side effects or nested transformations that hide intent.

### Углубление / follow-up

**Какая типичная ошибка связана с Comprehensions?**

A dense nested comprehension can be syntactically valid but harder to review and debug than a four-line loop.

## Expected answer rubric

### Must mention

- list/dict/set comprehensions
- generator expressions
- nested comprehensions
- scope

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- A dense nested comprehension can be syntactically valid but harder to review and debug than a four-line loop.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Comprehensions?

## Задача

### Email активных пользователей

Верни lower-case email активных пользователей с непустым email. Не изменяй вход.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A comprehension builds a list, dict or set from an expression, source iterable and optional filters; a generator expression stays lazy.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** A dense nested comprehension can be syntactically valid but harder to review and debug than a four-line loop.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
