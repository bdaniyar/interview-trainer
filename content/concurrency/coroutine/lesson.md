# Coroutine function and coroutine object

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Coroutine function and coroutine object**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``async def``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Coroutine function объявляется через `async def`; вызов создаёт coroutine object, а не выполняет тело до конца.

### Как работает

Объект запускается через `await` или scheduling как Task. Потерянная coroutine обычно приводит к warning `coroutine was never awaited`.


### Важный нюанс / ограничение

Coroutine object одноразовый: после завершения его нельзя await повторно.

## Модель понимания

Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `async def`
- calling async function
- coroutine object
- выполнение начинается после ожидания через await или планирования

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Coroutine function and coroutine object: отдельный пример

```python
import asyncio

async def answer():
    return 42

coroutine = answer()
print(type(coroutine).__name__)
print(asyncio.run(coroutine))
```

Вызов `async def` создаёт coroutine object; event loop выполняет его до результата.

## Типичные ошибки

### Ошибка 1

Возврат coroutine object из кода, обещавшего готовое значение, переносит async boundary не тому caller.

## Практика

**A · Предсказание результата.** Измени один input в примере ``async def`` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `calling async function`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие ``async def``, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Coroutine function and coroutine object за 45–60 секунд и назови одно ограничение.

## Предсказание результата кода

### Вызов async def

```python
async def answer():
    return 42
value = answer()
print(type(value).__name__)
value.close()
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
coroutine
```

Вызов async def создаёт coroutine object; выполнение требует await/event loop.

Типичная ошибка мышления: `coroutine-object`.

</details>

## Вопросы с собеседований

### Основной вопрос

Что такое Coroutine function and coroutine object и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Coroutine function and coroutine object?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Coroutine function объявляется через `async def`; вызов создаёт coroutine object, а не выполняет тело до конца.

### Нормальный ответ уровня Junior

> Coroutine function объявляется через `async def`; вызов создаёт coroutine object, а не выполняет тело до конца. Объект запускается через `await` или scheduling как Task. Потерянная coroutine обычно приводит к warning `coroutine was never awaited`. Важное ограничение: Coroutine object одноразовый: после завершения его нельзя await повторно.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Coroutine function and coroutine object?**

Возврат coroutine object из кода, обещавшего готовое значение, переносит async boundary не тому caller.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `async def`
- calling async function
- coroutine object
- выполнение начинается после ожидания через await или планирования

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Возврат coroutine object из кода, обещавшего готовое значение, переносит async boundary не тому caller.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Coroutine function and coroutine object?

## Задача

### Coroutine result

Реализуй async fetch_name(client,user_id): await client.get_user и верни name.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Coroutine function объявляется через `async def`; вызов создаёт coroutine object, а не выполняет тело до конца.
- **Механизм:** Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.
- **Ограничение:** Возврат coroutine object из кода, обещавшего готовое значение, переносит async boundary не тому caller.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [asyncio](https://docs.python.org/3.12/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html)

Последняя проверка версий: **2026-08-27**.
