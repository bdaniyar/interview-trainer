# Cancellation

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cancellation**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``CancelledError``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**`CancelledError`.** Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.

**cleanup.** `cleanup` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**cooperative cancellation.** Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.

**do not swallow cancellation accidentally.** Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``CancelledError`` и `cleanup` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``CancelledError``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `CancelledError`
- cleanup
- cooperative cancellation
- do not swallow cancellation accidentally

### Полезно

- связать Cancellation с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Cancellation: отдельный пример

```python
import asyncio

async def worker():
    try:
        await asyncio.sleep(10)
    finally:
        print("cleanup")

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(0)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")

asyncio.run(main())
```

Cancellation проходит через await, выполняет `finally` и обычно повторно распространяется caller.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``CancelledError`` до запуска.

**B · Find the bug.** Найди нарушение `cleanup` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Cancellation за 60 секунд: определение, механизм, пример, ограничение.

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

## Interview questions

### Основной вопрос

Что такое Cancellation и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Cancellation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Cancellation: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> Cancellation — тема, в которой я сначала фиксирую ``CancelledError``, затем объясняю `cleanup` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Cancellation?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- `CancelledError`
- cleanup
- cooperative cancellation
- do not swallow cancellation accidentally

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Cancellation?

## Задача

### Cancel and wait

Отмени task, await его, поглоти только CancelledError и верни True при отмене.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Cancellation: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
