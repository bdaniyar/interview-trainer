# Blocking code inside async code

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Blocking code inside async code**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``time.sleep``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Как работает

Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup.

**`time.sleep`.** ``time.sleep`` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**`requests`.** ``requests`` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**synchronous DB driver.** `synchronous DB driver` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**CPU-heavy loop.** `CPU-heavy loop` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**альтернативы: асинхронный клиент, `to_thread`, отдельный обработчик или процесс.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй ``time.sleep`` и ``requests`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``time.sleep``; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop

### Полезно

- альтернативы: асинхронный клиент, `to_thread`, отдельный обработчик или процесс

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для ``time.sleep`` до запуска.

**B · Найди ошибку.** Найди нарушение ``requests`` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Blocking code inside async code за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Отладка

### Blocking HTTP

**Сценарий:** requests.get внутри async route блокирует loop.

**Критерии ответа:** Async client или to_thread; timeout/cancellation.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### time.sleep in async

**Сценарий:** Все concurrent requests замирают.

**Критерии ответа:** asyncio.sleep для cooperative wait.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Blocking code inside async code и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Blocking code inside async code: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Нормальный ответ уровня Junior

> Blocking code inside async code — тема, в которой я сначала фиксирую ``time.sleep``, затем объясняю ``requests`` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `time.sleep`
- `requests`
- synchronous DB driver
- CPU-heavy loop

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Blocking code inside async code?

## Задача

### Вынести blocking call

Реализуй async call_blocking(function,*args,**kwargs) через asyncio.to_thread.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Blocking code inside async code: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
