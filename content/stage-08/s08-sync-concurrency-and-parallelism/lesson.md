# Sync, concurrency and parallelism

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Sync, concurrency and parallelism**, а не только запомнить термин;
- прочитать и изменить короткий пример для `sequential execution`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Sequential code does one operation after another; concurrency makes progress on multiple tasks; parallelism executes work simultaneously.

### Как работает

Async and threads often provide concurrency for I/O waits, while processes can provide parallel execution for CPU-bound Python.


### Важный нюанс / limitation

Concurrency can reduce idle time but adds ordering, cancellation and shared-state concerns; it does not make a single CPU calculation faster by itself.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- sequential execution
- concurrency
- parallelism
- I/O-bound

### Полезно

- CPU-bound

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Sync, concurrency and parallelism: отдельный пример

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    print(await asyncio.gather(fetch("a", 0.02), fetch("b", 0.01)))

asyncio.run(main())
```

Concurrency перекрывает ожидание двух I/O операций; это не параллельное выполнение CPU-bound Python.

## Common mistakes

### Ошибка 1

Selecting async for CPU-heavy work without moving it off the event loop increases latency for every request.

## Practice

**A · Code/result prediction.** Change one input in the `sequential execution` example and predict the result before running it.

**B · Find the bug.** Find code that violates `concurrency` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `sequential execution` and add one edge-case test.

**E · Interview explanation.** Explain Sync, concurrency and parallelism in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Sync, concurrency and parallelism и как это работает?

### Follow-up

Какая типичная ошибка связана с Sync, concurrency and parallelism?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Sequential code does one operation after another; concurrency makes progress on multiple tasks; parallelism executes work simultaneously.

### Нормальный Junior answer

> Sequential code does one operation after another; concurrency makes progress on multiple tasks; parallelism executes work simultaneously. Async and threads often provide concurrency for I/O waits, while processes can provide parallel execution for CPU-bound Python. Важное ограничение: Concurrency can reduce idle time but adds ordering, cancellation and shared-state concerns; it does not make a single CPU calculation faster by itself.

### Углубление / follow-up

**Какая типичная ошибка связана с Sync, concurrency and parallelism?**

Selecting async for CPU-heavy work without moving it off the event loop increases latency for every request.

## Expected answer rubric

### Must mention

- sequential execution
- concurrency
- parallelism
- I/O-bound

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Selecting async for CPU-heavy work without moving it off the event loop increases latency for every request.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Sync, concurrency and parallelism?

## Задача

### Sync I/O вне event loop

Реализуй async run_blocking_calls(function, values) через asyncio.to_thread и gather; порядок результата как во входе.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Sequential code does one operation after another; concurrency makes progress on multiple tasks; parallelism executes work simultaneously.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Selecting async for CPU-heavy work without moving it off the event loop increases latency for every request.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
