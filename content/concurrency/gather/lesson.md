# `asyncio.gather`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **`asyncio.gather`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `concurrent waits`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Как работает

Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup.

**concurrent waits.** `concurrent waits` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**result order.** `result order` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**exceptions.** `exceptions` является частью lifecycle coroutine/task между scheduling, точки приостановки await, cancellation и cleanup; отдельный thread автоматически не появляется.

**comparison with sequential await.** `await` приостанавливает текущую coroutine и отдаёт управление event loop, пока awaitable не станет готов.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `concurrent waits` и `result order` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `concurrent waits`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- concurrent waits
- result order
- exceptions
- comparison with sequential await

### Полезно

- связать `asyncio.gather` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `concurrent waits` до запуска.

**B · Найди ошибку.** Найди нарушение `result order` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про `asyncio.gather` за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

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

Ожидаемый результат:

```text
['a', 'b']
```

Coroutines завершаются в разное время, но gather возвращает results в порядке awaitables.

Типичная ошибка мышления: `gather-order`.

</details>

## Практика: Отладка

### Sequential awaits

**Сценарий:** Независимые I/O выполняются по очереди.

**Критерии ответа:** gather/TaskGroup с bounded concurrency и failure policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое `asyncio.gather` и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`asyncio.gather`: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.

### Нормальный ответ уровня Junior

> `asyncio.gather` — тема, в которой я сначала фиксирую `concurrent waits`, затем объясняю `result order` на коротком примере. Ключевой механизм: Проследи coroutine от создания через scheduling и точки приостановки await до result, cancellation и cleanup. Главная практическая ошибка — Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?**

Выполнить blocking call в event loop или создать coroutine и не await/schedule её.

## Критерии хорошего ответа

### Что обязательно упомянуть

- concurrent waits
- result order
- exceptions
- comparison with sequential await

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме `asyncio.gather`?

## Задача

### gather с порядком

Запусти fetch(value) конкурентно для ids и верни results в порядке ids.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `asyncio.gather`: Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг точки приостановки await.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Выполнить blocking call в event loop или создать coroutine и не await/schedule её.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
