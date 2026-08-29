# Coroutine function and coroutine object

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Coroutine function and coroutine object**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``async def``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A coroutine function is declared with `async def`; calling it creates a coroutine object rather than executing the body to completion.

### Как работает

The object runs when awaited or scheduled as a Task. Dropping it without either usually produces a 'coroutine was never awaited' warning.


### Важный нюанс / limitation

A coroutine object is single-use and cannot be awaited again after completion.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `async def`
- calling async function
- coroutine object
- execution begins when awaited/scheduled

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Coroutine function and coroutine object: отдельный пример

```python
import asyncio

async def answer():
    return 42

coroutine = answer()
print(type(coroutine).__name__)
print(asyncio.run(coroutine))
```

Вызов `async def` создаёт coroutine object; event loop выполняет его до результата.

## Common mistakes

### Ошибка 1

Returning a coroutine object from code that promised a final value leaks the async boundary to the wrong caller.

## Practice

**A · Code/result prediction.** Change one input in the ``async def`` example and predict the result before running it.

**B · Find the bug.** Find code that violates `calling async function` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``async def`` and add one edge-case test.

**E · Interview explanation.** Explain Coroutine function and coroutine object in 45–60 seconds and include one limitation.

## Code prediction

### Вызов async def

```python
async def answer():
    return 42
value = answer()
print(type(value).__name__)
value.close()
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
coroutine
```

Вызов async def создаёт coroutine object; выполнение требует await/event loop.

Misconception: `coroutine-object`.

</details>

## Interview questions

### Основной вопрос

Что такое Coroutine function and coroutine object и как это работает?

### Follow-up

Какая типичная ошибка связана с Coroutine function and coroutine object?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A coroutine function is declared with `async def`; calling it creates a coroutine object rather than executing the body to completion.

### Нормальный Junior answer

> A coroutine function is declared with `async def`; calling it creates a coroutine object rather than executing the body to completion. The object runs when awaited or scheduled as a Task. Dropping it without either usually produces a 'coroutine was never awaited' warning. Важное ограничение: A coroutine object is single-use and cannot be awaited again after completion.

### Углубление / follow-up

**Какая типичная ошибка связана с Coroutine function and coroutine object?**

Returning a coroutine object from code that promised a final value leaks the async boundary to the wrong caller.

## Expected answer rubric

### Must mention

- `async def`
- calling async function
- coroutine object
- execution begins when awaited/scheduled

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning a coroutine object from code that promised a final value leaks the async boundary to the wrong caller.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Coroutine function and coroutine object?

## Задача

### Coroutine result

Реализуй async fetch_name(client,user_id): await client.get_user и верни name.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A coroutine function is declared with `async def`; calling it creates a coroutine object rather than executing the body to completion.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Returning a coroutine object from code that promised a final value leaks the async boundary to the wrong caller.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
