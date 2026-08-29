# Blocking code inside async code

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Blocking code inside async code**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``time.sleep``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**`time.sleep`.** ``time.sleep`` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**`requests`.** ``requests`` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**synchronous DB driver.** `synchronous DB driver` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**CPU-heavy loop.** `CPU-heavy loop` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**alternatives: async client, `to_thread`, worker/process.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``time.sleep`` и ``requests`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``time.sleep``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop

### Полезно

- alternatives: async client, `to_thread`, worker/process

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Blocking code inside async code: отдельный пример

```python
import asyncio
import time

def blocking_read():
    time.sleep(0.05)
    return "done"

async def main():
    result = await asyncio.to_thread(blocking_read)
    print(result)

asyncio.run(main())
```

`to_thread` выносит неизбежный blocking call из event-loop thread; async-native client предпочтительнее.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``time.sleep`` до запуска.

**B · Find the bug.** Найди нарушение ``requests`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Blocking code inside async code за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Blocking HTTP

**Сценарий:** requests.get внутри async route блокирует loop.

**Rubric:** Async client или to_thread; timeout/cancellation.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### time.sleep in async

**Сценарий:** Все concurrent requests замирают.

**Rubric:** asyncio.sleep для cooperative wait.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Blocking code inside async code и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Blocking code inside async code: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> Blocking code inside async code — тема, в которой я сначала фиксирую ``time.sleep``, затем объясняю ``requests`` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?

## Задача

### Вынести blocking call

Реализуй async call_blocking(function,*args,**kwargs) через asyncio.to_thread.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Blocking code inside async code: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
