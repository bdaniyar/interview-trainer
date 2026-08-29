# Threads vs processes vs async

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Threads vs processes vs async**, а не только запомнить термин;
- прочитать и изменить короткий пример для `many network waits → async`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**many network waits → async.** `many network waits → async` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**blocking I/O library → thread pool.** Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

**CPU-bound pure Python → process pool/worker.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

**durable background job → queue/worker.** `durable background job → queue/worker` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `many network waits → async` и `blocking I/O library → thread pool` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `many network waits → async`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- many network waits → async
- blocking I/O library → thread pool
- CPU-bound pure Python → process pool/worker
- durable background job → queue/worker

### Полезно

- связать Threads vs processes vs async с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Threads vs processes vs async: отдельный пример

```python
decision = {
    "many_network_waits": "asyncio",
    "blocking_library": "threads",
    "cpu_bound_python": "processes",
}
print(decision)
```

Модель конкурентности выбирают по workload, isolation и цене communication, а не по моде.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `many network waits → async` до запуска.

**B · Find the bug.** Найди нарушение `blocking I/O library → thread pool` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Threads vs processes vs async за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Threads vs processes vs async и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Threads vs processes vs async: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> Threads vs processes vs async — тема, в которой я сначала фиксирую `many network waits → async`, затем объясняю `blocking I/O library → thread pool` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- many network waits → async
- blocking I/O library → thread pool
- CPU-bound pure Python → process pool/worker
- durable background job → queue/worker

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?

## Задача

### Ограничить concurrency

Реализуй map_limited через Semaphore и gather. Сохрани порядок; limit <= 0 вызывает ValueError.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Threads vs processes vs async: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
