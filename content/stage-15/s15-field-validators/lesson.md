# Field validators

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- объяснить `modern v2 validator API` своими словами и связать с backend-сценарием;
- объяснить `before/after` своими словами и связать с backend-сценарием;
- объяснить `avoid DB I/O inside schema validation.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Pydantic v2 преобразует и валидирует данные на границе; модель должна явно описывать required, nullable и default semantics.

В теме **Field validators** важно уверенно объяснять следующие части:

### modern v2 validator API

Для `modern v2 validator API` различай missing, explicit null, invalid input и serialized output Pydantic v2.

### before/after

Для `before/after` различай missing, explicit null, invalid input и serialized output Pydantic v2.

### avoid DB I/O inside schema validation

Для `avoid DB I/O inside schema validation` различай missing, explicit null, invalid input и serialized output Pydantic v2.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from pydantic import BaseModel, Field

class BookingCreate(BaseModel):
    room_id: int = Field(gt=0)
    guests: int = Field(ge=1, le=8)
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Путать str | None с полем, которое можно полностью не передать.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Field validators** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проверь missing, explicit null, неверный тип и сериализованный результат. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- modern v2 validator API
- before/after
- avoid DB I/O inside schema validation.
- Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Путать str | None с полем, которое можно полностью не передать.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- modern v2 validator API
- before/after
- avoid DB I/O inside schema validation.

## Задача

### Email field validator

LoginInput.email: before validator делает strip/lower; требует ровно один @ и непустые части.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Field validators**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
