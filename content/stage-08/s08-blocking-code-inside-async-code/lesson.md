# Blocking code inside async code

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить ``time.sleep`` своими словами и связать с backend-сценарием;
- объяснить ``requests`` своими словами и связать с backend-сценарием;
- объяснить `synchronous DB driver` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **Blocking code inside async code** важно уверенно объяснять следующие части:

### `time.sleep`

Для ``time.sleep`` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### `requests`

Для ``requests`` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### synchronous DB driver

Для `synchronous DB driver` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### CPU-heavy loop

Для `CPU-heavy loop` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### alternatives: async client, `to_thread`, worker/process

Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

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

1. Объясни **Blocking code inside async code** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop
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

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop
- alternatives: async client, `to_thread`, worker/process.

## Задача

### Вынести blocking call

Реализуй async call_blocking(function,*args,**kwargs) через asyncio.to_thread.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Debugging practice

### Blocking HTTP

**Сценарий:** requests.get внутри async route блокирует loop.

**Rubric:** Async client или to_thread; timeout/cancellation.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### time.sleep in async

**Сценарий:** Все concurrent requests замирают.

**Rubric:** asyncio.sleep для cooperative wait.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Blocking code inside async code**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
