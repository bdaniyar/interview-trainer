# Sync, concurrency and parallelism

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `sequential execution` своими словами и связать с backend-сценарием;
- объяснить `concurrency` своими словами и связать с backend-сценарием;
- объяснить `parallelism` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **Sync, concurrency and parallelism** важно уверенно объяснять следующие части:

### sequential execution

Для `sequential execution` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### concurrency

Для `concurrency` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### parallelism

Для `parallelism` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### I/O-bound

Для `I/O-bound` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### CPU-bound

Для `CPU-bound` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Sync, concurrency and parallelism** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- sequential execution
- concurrency
- parallelism
- I/O-bound
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

- sequential execution
- concurrency
- parallelism
- I/O-bound
- CPU-bound.

## Задача

### Sync I/O вне event loop

Реализуй async run_blocking_calls(function, values) через asyncio.to_thread и gather; порядок результата как во входе.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Sync, concurrency and parallelism**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
