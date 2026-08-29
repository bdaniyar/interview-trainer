# Threads vs processes vs async

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `many network waits → async` своими словами и связать с backend-сценарием;
- объяснить `blocking I/O library → thread pool` своими словами и связать с backend-сценарием;
- объяснить `CPU-bound pure Python → process pool/worker` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **Threads vs processes vs async** важно уверенно объяснять следующие части:

### many network waits → async

Для `many network waits → async` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### blocking I/O library → thread pool

Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

### CPU-bound pure Python → process pool/worker

Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

### durable background job → queue/worker

Для `durable background job → queue/worker` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Threads vs processes vs async** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- many network waits → async
- blocking I/O library → thread pool
- CPU-bound pure Python → process pool/worker
- durable background job → queue/worker.
- Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- many network waits → async
- blocking I/O library → thread pool
- CPU-bound pure Python → process pool/worker
- durable background job → queue/worker.

## Задача

### Ограничить concurrency

Реализуй map_limited через Semaphore и gather. Сохрани порядок; limit <= 0 вызывает ValueError.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Threads vs processes vs async**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
