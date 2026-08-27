# `asyncio.gather`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить `concurrent waits` своими словами и связать с backend-сценарием;
- объяснить `result order` своими словами и связать с backend-сценарием;
- объяснить `exceptions` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **`asyncio.gather`** важно уверенно объяснять следующие части:

### concurrent waits

Для `concurrent waits` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### result order

Для `result order` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### exceptions

Для `exceptions` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### comparison with sequential await

`await` приостанавливает текущую coroutine и отдаёт управление event loop, пока awaitable не станет готов.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
import asyncio

async def load_pair(client):
    first, second = await asyncio.gather(
        client.get("/users/1"),
        client.get("/users/2"),
    )
    return first, second
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **`asyncio.gather`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- concurrent waits
- result order
- exceptions
- comparison with sequential await.
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

- concurrent waits
- result order
- exceptions
- comparison with sequential await.

## Задача

### gather с порядком

Запусти fetch(value) конкурентно для ids и верни results в порядке ids.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### gather сохраняет порядок результатов

```python
import asyncio
async def item(value, delay):
    await asyncio.sleep(delay)
    return value
async def main():
    print(await asyncio.gather(item('a', .01), item('b', 0)))
asyncio.run(main())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
['a', 'b']
```

Coroutines завершаются в разное время, но gather возвращает results в порядке awaitables.

Misconception: `gather-order`.

</details>

## Debugging practice

### Sequential awaits

**Сценарий:** Независимые I/O выполняются по очереди.

**Rubric:** gather/TaskGroup с bounded concurrency и failure policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`asyncio.gather`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
