# Threads vs processes vs async

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Threads vs processes vs async**, а не только запомнить термин;
- прочитать и изменить короткий пример для `many network waits → async`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Как работает

Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup.

**many network waits → async.** `many network waits → async` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**blocking I/O library → thread pool.** Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

**Вычислительный код на чистом Python → пул процессов или отдельный обработчик.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

**надёжная фоновая задача → очередь и обработчик.** `durable background job → queue/worker` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `many network waits → async` и `blocking I/O library → thread pool` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `many network waits → async`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- many network waits → async
- blocking I/O library → thread pool
- Вычислительный код на чистом Python → пул процессов или отдельный обработчик
- надёжная фоновая задача → очередь и обработчик

### Полезно

- связать Threads vs processes vs async с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Threads vs processes vs async: отдельный пример

```python
decision = {
    "many_network_waits": "asyncio",
    "blocking_library": "threads",
    "cpu_bound_python": "processes",
}
print(decision)
```

Модель конкурентности выбирают по workload, isolation и цене communication, а не по моде.

## Типичные ошибки

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `many network waits → async` до запуска.

**B · Найди ошибку.** Найди нарушение `blocking I/O library → thread pool` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Threads vs processes vs async за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Threads vs processes vs async и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Threads vs processes vs async: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Нормальный ответ уровня Junior

> Threads vs processes vs async — тема, в которой я сначала фиксирую `many network waits → async`, затем объясняю `blocking I/O library → thread pool` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Критерии хорошего ответа

### Что обязательно упомянуть

- many network waits → async
- blocking I/O library → thread pool
- Вычислительный код на чистом Python → пул процессов или отдельный обработчик
- надёжная фоновая задача → очередь и обработчик

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Threads vs processes vs async?

## Задача

### Ограничить concurrency

Реализуй map_limited через Semaphore и gather. Сохрани порядок; limit <= 0 вызывает ValueError.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Threads vs processes vs async: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
