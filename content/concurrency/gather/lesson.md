# `asyncio.gather`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`asyncio.gather`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `concurrent waits`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**concurrent waits.** `concurrent waits` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**result order.** `result order` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**exceptions.** `exceptions` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**comparison with sequential await.** `await` приостанавливает текущую coroutine и отдаёт управление event loop, пока awaitable не станет готов.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `concurrent waits` и `result order` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `concurrent waits`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- concurrent waits
- result order
- exceptions
- comparison with sequential await

### Полезно

- связать `asyncio.gather` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `asyncio.gather`: отдельный пример

```python
import asyncio

async def item(value, delay):
    await asyncio.sleep(delay)
    return value

async def main():
    result = await asyncio.gather(item("first", 0.02), item("second", 0))
    print(result)

asyncio.run(main())
```

`gather` запускает операции конкурентно, но возвращает результаты в порядке переданных awaitables.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `concurrent waits` до запуска.

**B · Find the bug.** Найди нарушение `result order` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `asyncio.gather` за 60 секунд: определение, механизм, пример, ограничение.

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

## Interview questions

### Основной вопрос

Что такое `asyncio.gather` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`asyncio.gather`: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> `asyncio.gather` — тема, в которой я сначала фиксирую `concurrent waits`, затем объясняю `result order` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- concurrent waits
- result order
- exceptions
- comparison with sequential await

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?

## Задача

### gather с порядком

Запусти fetch(value) конкурентно для ids и верни results в порядке ids.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `asyncio.gather`: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
