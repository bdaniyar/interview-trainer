# Yield dependencies

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Yield dependencies**, а не только запомнить термин;
- прочитать и изменить короткий пример для `setup/cleanup`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**setup/cleanup.** `setup/cleanup` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**session lifecycle.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

**exception behavior.** `exception behavior` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `setup/cleanup` и `session lifecycle` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `setup/cleanup`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- setup/cleanup
- session lifecycle
- exception behavior

### Полезно

- связать Yield dependencies с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Yield dependencies: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
events = []
# Добавь yield dependency и endpoint.
```

Это публичный starter contract практики «Yield dependency cleanup». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `setup/cleanup` до запуска.

**B · Find the bug.** Найди нарушение `session lifecycle` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Yield dependencies за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Yield dependencies и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Yield dependencies?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Yield dependencies: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Нормальный Junior answer

> Yield dependencies — тема, в которой я сначала фиксирую `setup/cleanup`, затем объясняю `session lifecycle` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Yield dependencies?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Expected answer rubric

### Must mention

- setup/cleanup
- session lifecycle
- exception behavior

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Yield dependencies?

## Задача

### Yield dependency cleanup

get_resource пишет open/close в events; GET /resource получает yielded db.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Yield dependencies: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
