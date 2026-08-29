# `await` and cooperative scheduling

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`await` and cooperative scheduling**, а не только запомнить термин;
- прочитать и изменить короткий пример для `suspension point`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`await` приостанавливает текущую coroutine до готовности awaitable и позволяет event loop выполнять другие готовые tasks. Это кооперативная конкурентность, а не автоматический новый thread или parallel CPU execution.

### Как работает

`async def` при вызове создаёт coroutine object. Когда coroutine запущена task-ом, она выполняется до `await`. Если awaitable ещё не готов, task сохраняет state и уступает loop; после события продолжает со следующей строки.


### Пример

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    result = await asyncio.gather(fetch("profile", 0.02), fetch("orders", 0.01))
    print(result)  # ['profile', 'orders']

asyncio.run(main())
```

### Важный нюанс / limitation

Два последовательных `await` остаются последовательными. Конкурентный запуск требует tasks/`gather`/`TaskGroup`. `time.sleep`, sync DB driver или CPU loop внутри async endpoint блокирует весь event-loop thread.

### Где используется в backend

Async endpoint полезен, когда весь I/O path — HTTP client, DB driver, queue — предоставляет awaitable API.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- coroutine object
- suspension point
- event loop
- последовательный vs concurrent await
- blocking code

### Полезно

- create_task/gather
- cancellation cleanup
- timeouts

### Можно не учить глубоко

- реализация selectors/proactors и bytecode coroutine

## Code examples

### `await` and cooperative scheduling: отдельный пример

```python
import asyncio

async def worker(name):
    print(name, "start")
    await asyncio.sleep(0)
    print(name, "resume")

async def main():
    await asyncio.gather(worker("a"), worker("b"))

asyncio.run(main())
```

Task уступает управление только в await point, после чего loop может продолжить другую ready task.

## Common mistakes

### Ошибка 1

Вызвать coroutine без `await`: работа не выполнится, возможен warning `coroutine was never awaited`.

### Ошибка 2

Использовать `time.sleep()` в `async def`; нужно `await asyncio.sleep()` или вынести blocking call.

### Ошибка 3

Ожидать две независимые операции последовательно и называть это concurrent execution.

## Practice

**A · Code prediction.** Определи порядок вывода двух tasks с `sleep(0)`.

**B · Find the bug.** Найди `requests.get`/`time.sleep` внутри async endpoint.

**C · Rewrite.** Запусти независимые I/O calls через `gather`.

**D · Small task.** Реализуй bounded async fetch с timeout.

## Code prediction

### Await сохраняет порядок внутри task

```python
import asyncio
async def main():
    print('a')
    await asyncio.sleep(0)
    print('b')
asyncio.run(main())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
a
b
```

await может отдать управление loop, но эта программа содержит только одну пользовательскую task.

Misconception: `await-order`.

</details>

## Debugging practice

### Forgotten await

**Сценарий:** Endpoint возвращает coroutine object.

**Rubric:** await coroutine; включить warnings/test serialization.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что делает `await` и создаёт ли он конкурентность автоматически?

### Follow-up

Что произойдёт, если вызвать blocking функцию внутри event loop?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Await приостанавливает текущую coroutine и отдаёт loop управление; сам по себе он не создаёт thread и два последовательных await не становятся concurrent.

### Нормальный Junior answer

> `await` работает внутри coroutine: если операция не готова, state текущей task сохраняется, а event loop может выполнять другие tasks. После готовности выполнение продолжится со следующей строки. Это полезно для I/O-bound кода. Один await не создаёт новую task, поэтому для независимых операций нужны `create_task`, `gather` или `TaskGroup`.

### Углубление / follow-up

**Что произойдёт, если вызвать blocking функцию внутри event loop?**

Она не отдаёт управление, поэтому задержит все tasks этого loop; нужен async-native API, `to_thread` для blocking I/O или отдельный process/worker для CPU work.

## Expected answer rubric

### Must mention

- coroutine object
- suspension point
- event loop
- последовательный vs concurrent await

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Вызвать coroutine без `await`: работа не выполнится, возможен warning `coroutine was never awaited`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Что произойдёт, если вызвать blocking функцию внутри event loop?

## Задача

### Конкурентный profile

Реализуй load_profile: get_user и get_roles запускаются конкурентно; верни объединённый dict.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Await приостанавливает текущую coroutine и отдаёт loop управление; сам по себе он не создаёт thread и два последовательных await не становятся concurrent.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Вызвать coroutine без `await`: работа не выполнится, возможен warning `coroutine was never awaited`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
