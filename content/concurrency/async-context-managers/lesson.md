# Async context managers

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Async context managers**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``async with``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Как работает

Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup.

**`async with`.** ``async with`` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**жизненный цикл соединения, сессии или клиента.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

**`__aenter__`/`__aexit__`.** ``__aenter__`/`__aexit__`` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй ``async with`` и `connection/session/client lifecycle` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``async with``; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `async with`
- жизненный цикл соединения, сессии или клиента
- `__aenter__`/`__aexit__`

### Полезно

- связать Async context managers с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

Async Контекстный менеджер разрешает await во время acquire/release и гарантирует cleanup вокруг блока.

## Типичные ошибки

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для ``async with`` до запуска.

**B · Найди ошибку.** Найди нарушение `connection/session/client lifecycle` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Async context managers за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Async context managers и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Async context managers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Async context managers: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Нормальный ответ уровня Junior

> Async context managers — тема, в которой я сначала фиксирую ``async with``, затем объясняю `connection/session/client lifecycle` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Async context managers?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `async with`
- жизненный цикл соединения, сессии или клиента
- `__aenter__`/`__aexit__`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Async context managers?

## Задача

### Async resource manager

await opener при enter, await closer(resource) при exit, исключение не подавляй.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Async context managers: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
