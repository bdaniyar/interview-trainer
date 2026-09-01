# Project structure

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Project structure**, а не только запомнить термин;
- прочитать и изменить короткий пример для `routers`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Практичная структура FastAPI отделяет HTTP routers и schemas от use-case services и деталей data access.

### Как работает

Routers адаптируют request/response, services содержат business workflow и transaction decisions, repositories или query modules изолируют persistence, когда добавляют реальную ценность.


### Важный нюанс / ограничение

Не создавай pass-through layers без поведения: boundary должна соответствовать изменению или test seam.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- routers
- schemas
- services
- repositories/data access

### Полезно

- dependencies
- settings

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Project structure: отдельный пример

```python
def example_s14_project_structure() -> tuple[str, ...]:
    # Project structure: проверяем отдельный contract урока.
    return ('routers', 'schemas', 'services', 'repositories/data access',)

assert example_s14_project_structure()
```

Проследи request через router, validation, dependency, service и response model.

## Типичные ошибки

### Ошибка 1

Все concerns внутри routes усложняют transaction tests и проверку business logic без framework.

## Практика

**A · Предсказание результата.** Измени один input в примере `routers` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `schemas`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `routers`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Project structure за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Project structure и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Project structure?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Практичная структура FastAPI отделяет HTTP routers и schemas от use-case services и деталей data access.

### Нормальный ответ уровня Junior

> Практичная структура FastAPI отделяет HTTP routers и schemas от use-case services и деталей data access. Routers адаптируют request/response, services содержат business workflow и transaction decisions, repositories или query modules изолируют persistence, когда добавляют реальную ценность. Важное ограничение: Не создавай pass-through layers без поведения: boundary должна соответствовать изменению или test seam.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Project structure?**

Все concerns внутри routes усложняют transaction tests и проверку business logic без framework.

## Критерии хорошего ответа

### Что обязательно упомянуть

- routers
- schemas
- services
- repositories/data access

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Все concerns внутри routes усложняют transaction tests и проверку business logic без framework.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Project structure?

## Задача

Сделай короткую письменную практику по теме **Project structure**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Практичная структура FastAPI отделяет HTTP routers и schemas от use-case services и деталей data access.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Все concerns внутри routes усложняют transaction tests и проверку business logic без framework.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
