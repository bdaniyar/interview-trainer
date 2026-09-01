# Tasks and `asyncio.create_task`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Tasks and `asyncio.create_task`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `scheduling`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Asyncio Task планирует одну coroutine и хранит её состояние завершения, result, exception или cancellation.

### Как работает

`create_task` делает coroutine готовой к выполнению; caller должен сохранить reference и затем дождаться результата либо явно обработать outcome.


### Важный нюанс / ограничение

Fire-and-forget внутри web process не является durable: shutdown может потерять task, а необработанное исключение останется только в logs.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- scheduling
- keeping references
- awaiting completion
- exception handling

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Tasks and `asyncio.create_task`: отдельный пример

```python
import asyncio

async def save():
    await asyncio.sleep(0)
    return "saved"

async def main():
    task = asyncio.create_task(save(), name="save-user")
    print(task.get_name())
    print(await task)

asyncio.run(main())
```

Task планирует coroutine и хранит её completion/result; reference нужно сохранить и дождаться.

## Типичные ошибки

### Ошибка 1

Создание task без сохранения reference скрывает сбои и не гарантирует завершение до остановки request или process.

## Практика

**A · Предсказание результата.** Измени один input в примере `scheduling` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `keeping references`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `scheduling`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Tasks and `asyncio.create_task` за 45–60 секунд и назови одно ограничение.

## Предсказание результата кода

### create_task планирует работу

```python
import asyncio
async def child():
    print('child')
async def main():
    task = asyncio.create_task(child())
    print('parent')
    await task
asyncio.run(main())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
parent
child
```

create_task ставит coroutine в планирование; текущая task продолжает до await.

Типичная ошибка мышления: `task-scheduling`.

</details>

## Практика: Отладка

### Unhandled task

**Сценарий:** create_task потерян, exception logged later.

**Критерии ответа:** Хранить reference, await/supervise, done callback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Tasks and `asyncio.create_task` и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Tasks and `asyncio.create_task`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Asyncio Task планирует одну coroutine и хранит её состояние завершения, result, exception или cancellation.

### Нормальный ответ уровня Junior

> Asyncio Task планирует одну coroutine и хранит её состояние завершения, result, exception или cancellation. `create_task` делает coroutine готовой к выполнению; caller должен сохранить reference и затем дождаться результата либо явно обработать outcome. Важное ограничение: Fire-and-forget внутри web process не является durable: shutdown может потерять task, а необработанное исключение останется только в logs.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Tasks and `asyncio.create_task`?**

Создание task без сохранения reference скрывает сбои и не гарантирует завершение до остановки request или process.

## Критерии хорошего ответа

### Что обязательно упомянуть

- scheduling
- keeping references
- awaiting completion
- exception handling

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Создание task без сохранения reference скрывает сбои и не гарантирует завершение до остановки request или process.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Tasks and `asyncio.create_task`?

## Задача

### Task lifecycle registry

Создай task, добавь в registry set, удали done callback и верни task.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Asyncio Task планирует одну coroutine и хранит её состояние завершения, result, exception или cancellation.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Создание task без сохранения reference скрывает сбои и не гарантирует завершение до остановки request или process.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
