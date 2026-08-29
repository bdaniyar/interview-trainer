# `*args`, `**kwargs` and unpacking

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`*args`, `**kwargs` and unpacking**, а не только запомнить термин;
- прочитать и изменить короткий пример для `collection`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict; the same stars unpack values at a call site.

### Как работает

Argument binding still enforces the signature. Forwarding wrappers commonly call `fn(*args, **kwargs)`, and duplicate values for one parameter raise `TypeError`.


### Важный нюанс / limitation

Do not replace a clear public signature with unlimited kwargs. Explicit keyword-only parameters produce better typing and API errors.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- collection
- forwarding
- iterable/dict unpacking
- duplicate arguments

### Полезно

- wrapper functions

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### `*args`, `**kwargs` and unpacking: отдельный пример

```python
def audit(event, *entity_ids, request_id=None, **details):
    return event, entity_ids, request_id, details

context = {"request_id": "req-7", "actor": 42}
print(audit("updated", 10, 11, **context))
```

`*args` собирает positional IDs, `**kwargs` — дополнительные named fields; unpacking разворачивает mapping при вызове.

## Common mistakes

### Ошибка 1

Forwarding `fn(value, **{'value': other})` passes the same parameter twice and raises `TypeError`.

## Practice

**A · Code/result prediction.** Change one input in the `collection` example and predict the result before running it.

**B · Find the bug.** Find code that violates `forwarding` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `collection` and add one edge-case test.

**E · Interview explanation.** Explain `*args`, `**kwargs` and unpacking in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое `*args`, `**kwargs` and unpacking и как это работает?

### Follow-up

Какая типичная ошибка связана с `*args`, `**kwargs` and unpacking?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict; the same stars unpack values at a call site.

### Нормальный Junior answer

> `*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict; the same stars unpack values at a call site. Argument binding still enforces the signature. Forwarding wrappers commonly call `fn(*args, **kwargs)`, and duplicate values for one parameter raise `TypeError`. Важное ограничение: Do not replace a clear public signature with unlimited kwargs. Explicit keyword-only parameters produce better typing and API errors.

### Углубление / follow-up

**Какая типичная ошибка связана с `*args`, `**kwargs` and unpacking?**

Forwarding `fn(value, **{'value': other})` passes the same parameter twice and raises `TypeError`.

## Expected answer rubric

### Must mention

- collection
- forwarding
- iterable/dict unpacking
- duplicate arguments

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Forwarding `fn(value, **{'value': other})` passes the same parameter twice and raises `TypeError`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с `*args`, `**kwargs` and unpacking?

## Задача

### Объединить options

Объедини base и keyword overrides, где overrides побеждают. Не изменяй входной dict.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict; the same stars unpack values at a call site.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Forwarding `fn(value, **{'value': other})` passes the same parameter twice and raises `TypeError`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
