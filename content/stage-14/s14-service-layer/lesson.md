# Service layer

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Service layer**, а не только запомнить термин;
- прочитать и изменить короткий пример для `domain/use-case logic`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**domain/use-case logic.** `domain/use-case logic` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**transaction boundary.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**framework-independent testing.** `framework-independent testing` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `domain/use-case logic` и `transaction boundary` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `domain/use-case logic`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- domain/use-case logic
- transaction boundary
- framework-independent testing

### Полезно

- связать Service layer с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Service layer: отдельный пример

```text
Сценарий: Route пишет current_user в module global.

Проверка:
Request-scoped dependency/context, immutable arguments; concurrent test обнаруживает утечку между запросами.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `domain/use-case logic` до запуска.

**B · Найди ошибку.** Найди нарушение `transaction boundary` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Service layer за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Отладка

### Global request state

**Сценарий:** Route пишет current_user в module global.

**Критерии ответа:** Request-scoped dependency/context, immutable arguments; concurrent test обнаруживает утечку между запросами.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Service layer и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Service layer?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Service layer: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Нормальный ответ уровня Junior

> Service layer — тема, в которой я сначала фиксирую `domain/use-case logic`, затем объясняю `transaction boundary` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Service layer?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Критерии хорошего ответа

### Что обязательно упомянуть

- domain/use-case logic
- transaction boundary
- framework-independent testing

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Service layer?

## Задача

Сделай короткую письменную практику по теме **Service layer**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Service layer: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
