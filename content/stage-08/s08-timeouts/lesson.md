# Timeouts

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Timeouts**, а не только запомнить термин;
- прочитать и изменить короткий пример для `bounded waiting`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Как работает

Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup.

**bounded waiting.** `bounded waiting` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**`asyncio.timeout` or version-appropriate API.** ``asyncio.timeout` or version-appropriate API` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**cleanup.** `cleanup` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `bounded waiting` и ``asyncio.timeout` or version-appropriate API` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `bounded waiting`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- bounded waiting
- `asyncio.timeout` or version-appropriate API
- cleanup

### Полезно

- связать Timeouts с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Timeouts: отдельный пример

```python
import asyncio

async def main():
    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(1)
    except TimeoutError:
        print("deadline exceeded")

asyncio.run(main())
```

Timeout задаёт deadline scope, отменяет затянувшееся ожидание и сообщает caller через `TimeoutError`.

## Типичные ошибки

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `bounded waiting` до запуска.

**B · Найди ошибку.** Найди нарушение ``asyncio.timeout` or version-appropriate API` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Timeouts за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Timeouts и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Timeouts?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Timeouts: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Нормальный ответ уровня Junior

> Timeouts — тема, в которой я сначала фиксирую `bounded waiting`, затем объясняю ``asyncio.timeout` or version-appropriate API` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Timeouts?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Критерии хорошего ответа

### Что обязательно упомянуть

- bounded waiting
- `asyncio.timeout` or version-appropriate API
- cleanup

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Timeouts?

## Задача

### Timeout boundary

Реализуй await_with_timeout(awaitable,seconds) через asyncio.timeout; TimeoutError не подавляй.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Timeouts: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
