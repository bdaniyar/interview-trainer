# Coroutine function and coroutine object

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- объяснить ``async def`` своими словами и связать с backend-сценарием;
- объяснить `calling async function` своими словами и связать с backend-сценарием;
- объяснить `coroutine object` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.

В теме **Coroutine function and coroutine object** важно уверенно объяснять следующие части:

### `async def`

Для ``async def`` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### calling async function

Для `calling async function` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.

### coroutine object

Вызов `async def` создаёт coroutine object; код начнёт выполняться при await или scheduling как Task.

### execution begins when awaited/scheduled

`await` приостанавливает текущую coroutine и отдаёт управление event loop, пока awaitable не станет готов.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Coroutine function and coroutine object** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `async def`
- calling async function
- coroutine object
- execution begins when awaited/scheduled.
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

- `async def`
- calling async function
- coroutine object
- execution begins when awaited/scheduled.

## Задача

### Coroutine result

Реализуй async fetch_name(client,user_id): await client.get_user и верни name.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
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

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Coroutine function and coroutine object**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
