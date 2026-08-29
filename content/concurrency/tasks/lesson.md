# Tasks and `asyncio.create_task`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Tasks and `asyncio.create_task`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `scheduling`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

An asyncio Task schedules one coroutine and stores its completion, result, exception or cancellation state.

### Как работает

`create_task` makes a coroutine eligible to run; the caller should keep a reference and eventually await it or otherwise handle its outcome.


### Важный нюанс / limitation

Fire-and-forget inside a web process is not durable: process shutdown can lose the task, and unobserved exceptions may surface only in logs.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- scheduling
- keeping references
- awaiting completion
- exception handling

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Tasks and `asyncio.create_task`: отдельный пример

```python
import asyncio

async def save():
    await asyncio.sleep(0)
    return "saved"

async def main():
    task = asyncio.create_task(save(), name="save-user")
    print(task.get_name())
    print(await task)

asyncio.run(main())
```

Task планирует coroutine и хранит её completion/result; reference нужно сохранить и дождаться.

## Common mistakes

### Ошибка 1

Creating a task and dropping the reference hides failures and does not guarantee completion before request/process shutdown.

## Practice

**A · Code/result prediction.** Change one input in the `scheduling` example and predict the result before running it.

**B · Find the bug.** Find code that violates `keeping references` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `scheduling` and add one edge-case test.

**E · Interview explanation.** Explain Tasks and `asyncio.create_task` in 45–60 seconds and include one limitation.

## Code prediction

### create_task планирует работу

```python
import asyncio
async def child():
    print('child')
async def main():
    task = asyncio.create_task(child())
    print('parent')
    await task
asyncio.run(main())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
parent
child
```

create_task ставит coroutine в планирование; текущая task продолжает до await.

Misconception: `task-scheduling`.

</details>

## Debugging practice

### Unhandled task

**Сценарий:** create_task потерян, exception logged later.

**Rubric:** Хранить reference, await/supervise, done callback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Tasks and `asyncio.create_task` и как это работает?

### Follow-up

Какая типичная ошибка связана с Tasks and `asyncio.create_task`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

An asyncio Task schedules one coroutine and stores its completion, result, exception or cancellation state.

### Нормальный Junior answer

> An asyncio Task schedules one coroutine and stores its completion, result, exception or cancellation state. `create_task` makes a coroutine eligible to run; the caller should keep a reference and eventually await it or otherwise handle its outcome. Важное ограничение: Fire-and-forget inside a web process is not durable: process shutdown can lose the task, and unobserved exceptions may surface only in logs.

### Углубление / follow-up

**Какая типичная ошибка связана с Tasks and `asyncio.create_task`?**

Creating a task and dropping the reference hides failures and does not guarantee completion before request/process shutdown.

## Expected answer rubric

### Must mention

- scheduling
- keeping references
- awaiting completion
- exception handling

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Creating a task and dropping the reference hides failures and does not guarantee completion before request/process shutdown.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Tasks and `asyncio.create_task`?

## Задача

### Task lifecycle registry

Создай task, добавь в registry set, удали done callback и верни task.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** An asyncio Task schedules one coroutine and stores its completion, result, exception or cancellation state.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Creating a task and dropping the reference hides failures and does not guarantee completion before request/process shutdown.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
