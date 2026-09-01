# Exception handlers

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Exception handlers**, а не только запомнить термин;
- прочитать и изменить короткий пример для `domain exception`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Exception handler преобразует определённый тип исключения в единый HTTP response на границе application или router.

### Как работает

Domain code поднимает domain exception, а FastAPI handler сопоставляет его со status и безопасным payload; неожиданные ошибки остаются server failures.


### Важный нюанс / ограничение

Не преобразуй любой Exception в 400: так programming bugs маскируются под ошибку client.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- domain exception
- HTTP mapping
- global handler
- avoid leaking internals

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Exception handlers: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь exception, handler и endpoint.
```

Это публичный starter contract практики «Domain exception handler». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Передача `str(database_error)` клиенту раскрывает SQL/schema details и создаёт нестабильный contract.

## Практика

**A · Предсказание результата.** Измени один input в примере `domain exception` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `HTTP mapping`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `domain exception`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Exception handlers за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Exception handlers и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Exception handlers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Exception handler преобразует определённый тип исключения в единый HTTP response на границе application или router.

### Нормальный ответ уровня Junior

> Exception handler преобразует определённый тип исключения в единый HTTP response на границе application или router. Domain code поднимает domain exception, а FastAPI handler сопоставляет его со status и безопасным payload; неожиданные ошибки остаются server failures. Важное ограничение: Не преобразуй любой Exception в 400: так programming bugs маскируются под ошибку client.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Exception handlers?**

Передача `str(database_error)` клиенту раскрывает SQL/schema details и создаёт нестабильный contract.

## Критерии хорошего ответа

### Что обязательно упомянуть

- domain exception
- HTTP mapping
- global handler
- avoid leaking internals

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Передача `str(database_error)` клиенту раскрывает SQL/schema details и создаёт нестабильный contract.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Exception handlers?

## Задача

### Domain exception handler

DomainConflict handler возвращает status 409 и JSON error; GET /conflict поднимает already booked.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Exception handler преобразует определённый тип исключения в единый HTTP response на границе application или router.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Передача `str(database_error)` клиенту раскрывает SQL/schema details и создаёт нестабильный contract.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
