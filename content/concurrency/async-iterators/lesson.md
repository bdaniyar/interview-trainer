# Async iterators and generators

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Async iterators and generators**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``async for``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**`async for`.** ``async for`` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**streaming.** `streaming` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**paginated I/O.** `paginated I/O` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**cleanup.** `cleanup` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``async for`` и `streaming` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``async for``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `async for`
- streaming
- paginated I/O
- cleanup

### Полезно

- связать Async iterators and generators с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Async iterators and generators: отдельный пример

```python
import asyncio

async def events():
    for value in range(3):
        await asyncio.sleep(0)
        yield value

async def main():
    async for event in events():
        print(event)

asyncio.run(main())
```

Async generator лениво выдаёт значения и может ожидать I/O между итерациями.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``async for`` до запуска.

**B · Find the bug.** Найди нарушение `streaming` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Async iterators and generators за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Async iterators and generators и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Async iterators and generators?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Async iterators and generators: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> Async iterators and generators — тема, в которой я сначала фиксирую ``async for``, затем объясняю `streaming` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Async iterators and generators?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- `async for`
- streaming
- paginated I/O
- cleanup

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Async iterators and generators?

## Задача

### AsyncRange

Реализуй async iterator, выдающий start..stop-1 и завершающийся StopAsyncIteration.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Async iterators and generators: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
