# Middleware

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Middleware**, а не только запомнить термин;
- прочитать и изменить короткий пример для `request/response wrapper`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Middleware оборачивает request/response flow для cross-cutting задач: request ID, timing или security headers.

### Как работает

Каждый middleware выполняется до внутреннего app и после его response; порядок влияет на наблюдение и обработку ошибок.


### Важный нюанс / ограничение

Domain authorization обычно требует resolved user/resource и относится к dependencies или services, а не к общему middleware.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- request/response wrapper
- timing/request ID
- ordering
- not for domain logic

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Middleware: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь middleware и endpoint.
```

Это публичный starter contract практики «Request-ID middleware». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Чтение streaming request body в middleware без восстановления потока может оставить endpoint без body.

## Практика

**A · Предсказание результата.** Измени один input в примере `request/response wrapper` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `timing/request ID`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `request/response wrapper`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Middleware за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Middleware и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Middleware?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Middleware оборачивает request/response flow для cross-cutting задач: request ID, timing или security headers.

### Нормальный ответ уровня Junior

> Middleware оборачивает request/response flow для cross-cutting задач: request ID, timing или security headers. Каждый middleware выполняется до внутреннего app и после его response; порядок влияет на наблюдение и обработку ошибок. Важное ограничение: Domain authorization обычно требует resolved user/resource и относится к dependencies или services, а не к общему middleware.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Middleware?**

Чтение streaming request body в middleware без восстановления потока может оставить endpoint без body.

## Критерии хорошего ответа

### Что обязательно упомянуть

- request/response wrapper
- timing/request ID
- ordering
- not for domain logic

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Чтение streaming request body в middleware без восстановления потока может оставить endpoint без body.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Middleware?

## Задача

### Request-ID middleware

Response X-Request-ID равен входному header либо новому UUID; GET /ping возвращает pong.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Middleware оборачивает request/response flow для cross-cutting задач: request ID, timing или security headers.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Чтение streaming request body в middleware без восстановления потока может оставить endpoint без body.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
