# Async context managers

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Async context managers**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``async with``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Как работает

Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.

**`async with`.** ``async with`` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.

**connection/session/client lifecycle.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

**`__aenter__`/`__aexit__`.** ``__aenter__`/`__aexit__`` является частью lifecycle coroutine/task между scheduling, await points, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``async with`` и `connection/session/client lifecycle` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``async with``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `async with`
- connection/session/client lifecycle
- `__aenter__`/`__aexit__`

### Полезно

- связать Async context managers с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Async context managers: отдельный пример

```python
class AsyncResource:
    async def __aenter__(self):
        return self

    async def __aexit__(self, kind, value, traceback):
        await self.close()

    async def close(self):
        pass
```

Async context manager разрешает await во время acquire/release и гарантирует cleanup вокруг блока.

## Common mistakes

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``async with`` до запуска.

**B · Find the bug.** Найди нарушение `connection/session/client lifecycle` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Async context managers за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Async context managers и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Async context managers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Async context managers: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.

### Нормальный Junior answer

> Async context managers — тема, в которой я сначала фиксирую ``async with``, затем объясняю `connection/session/client lifecycle` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Async context managers?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Expected answer rubric

### Must mention

- `async with`
- connection/session/client lifecycle
- `__aenter__`/`__aexit__`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Async context managers?

## Задача

### Async resource manager

await opener при enter, await closer(resource) при exit, исключение не подавляй.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Async context managers: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
