# Cancellation

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить ``CancelledError`` своими словами и связать с backend-сценарием;
- объяснить `cleanup` своими словами и связать с backend-сценарием;
- объяснить `cooperative cancellation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **Cancellation** важно уверенно объяснять следующие части:

### `CancelledError`

Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.

### cleanup

Для `cleanup` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### cooperative cancellation

Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.

### do not swallow cancellation accidentally

Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.

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

1. Объясни **Cancellation** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `CancelledError`
- cleanup
- cooperative cancellation
- do not swallow cancellation accidentally.
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

- `CancelledError`
- cleanup
- cooperative cancellation
- do not swallow cancellation accidentally.

## Задача

### Cancel and wait

Отмени task, await его, поглоти только CancelledError и верни True при отмене.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Timeout преобразует ожидание в ошибку

```python
import asyncio
async def main():
    try:
        await asyncio.wait_for(asyncio.sleep(1), timeout=0.001)
    except TimeoutError:
        print('timeout')
asyncio.run(main())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
timeout
```

wait_for отменяет слишком долгий awaitable и поднимает TimeoutError вызывающему коду.

Misconception: `async-timeout`.

</details>

## Debugging practice

### Swallowed cancellation

**Сценарий:** except BaseException подавляет shutdown.

**Rubric:** CancelledError не поглощать; cleanup finally; re-raise.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Cancellation**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
