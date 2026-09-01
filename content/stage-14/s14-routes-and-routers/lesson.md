# Routes and routers

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Routes and routers**, а не только запомнить термин;
- прочитать и изменить короткий пример для `decorator`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**decorator.** Decorator получает callable и возвращает callable; для framework route decorator также регистрирует функцию и её metadata во время импорта модуля.

**APIRouter.** `APIRouter` группирует связанные path operations и их общие prefix, tags или dependencies; router подключают к приложению через `include_router`, не создавая второе приложение.

**prefix.** Router prefix добавляется ко всем путям группы и позволяет собирать модульный API без повторения `/users` или `/v1` в каждом decorator.

**tags.** `tags` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**modular structure.** `modular structure` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `decorator` и `APIRouter` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `decorator`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- decorator
- APIRouter
- prefix
- tags

### Полезно

- modular structure

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Routes and routers: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь route.
```

Это публичный starter contract практики «Health route». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `decorator` до запуска.

**B · Найди ошибку.** Найди нарушение `APIRouter` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Routes and routers за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Routes and routers и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Routes and routers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Routes and routers: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Нормальный ответ уровня Junior

> Routes and routers — тема, в которой я сначала фиксирую `decorator`, затем объясняю `APIRouter` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Routes and routers?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Критерии хорошего ответа

### Что обязательно упомянуть

- decorator
- APIRouter
- prefix
- tags

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Routes and routers?

## Задача

### Health route

Создай FastAPI app с GET /health → 200 и JSON status=ok.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Routes and routers: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
