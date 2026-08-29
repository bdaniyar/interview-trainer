# Event loop

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Event loop**, а не только запомнить термин;
- прочитать и изменить короткий пример для `scheduling`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

The event loop schedules ready callbacks/tasks and waits for I/O readiness or timers when nothing is ready.

### Как работает

A task runs cooperatively until it awaits. The loop then resumes another ready task and later returns to the suspended one.


### Важный нюанс / limitation

One blocking function in the event-loop thread delays every other task on that loop.

### Где используется в backend

ASGI servers run application coroutines on event loops, so endpoint dependencies must respect the same boundary.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- scheduling
- readiness
- callbacks/tasks
- one blocking call stalls the loop

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Event loop: отдельный пример

```python
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_soon(future.set_result, "ready")
    print(await future)

asyncio.run(main())
```

Event loop выполняет ready callback, завершает Future и возобновляет ожидающую coroutine.

## Common mistakes

### Ошибка 1

Calling blocking network/DB code directly from an async endpoint stalls unrelated requests.

## Practice

**A · Code/result prediction.** Change one input in the `scheduling` example and predict the result before running it.

**B · Find the bug.** Find code that violates `readiness` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `scheduling` and add one edge-case test.

**E · Interview explanation.** Explain Event loop in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Event loop и как это работает?

### Follow-up

Какая типичная ошибка связана с Event loop?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

The event loop schedules ready callbacks/tasks and waits for I/O readiness or timers when nothing is ready.

### Нормальный Junior answer

> The event loop schedules ready callbacks/tasks and waits for I/O readiness or timers when nothing is ready. A task runs cooperatively until it awaits. The loop then resumes another ready task and later returns to the suspended one. Важное ограничение: One blocking function in the event-loop thread delays every other task on that loop.

### Углубление / follow-up

**Какая типичная ошибка связана с Event loop?**

Calling blocking network/DB code directly from an async endpoint stalls unrelated requests.

## Expected answer rubric

### Must mention

- scheduling
- readiness
- callbacks/tasks
- one blocking call stalls the loop

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Calling blocking network/DB code directly from an async endpoint stalls unrelated requests.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Event loop?

## Задача

### Cooperative checkpoint

append before, await asyncio.sleep(0), затем append after.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** The event loop schedules ready callbacks/tasks and waits for I/O readiness or timers when nothing is ready.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Calling blocking network/DB code directly from an async endpoint stalls unrelated requests.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
