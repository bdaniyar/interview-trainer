# Model validators

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Model validators**, а не только запомнить термин;
- прочитать и изменить короткий пример для `cross-field invariant`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат.

**cross-field invariant.** `cross-field invariant` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**validation ordering.** `validation ordering` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `cross-field invariant` и `validation ordering` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `cross-field invariant`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- cross-field invariant
- validation ordering

### Полезно

- связать Model validators с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Model validators: отдельный пример

```python
from pydantic import BaseModel

# Создай BookingPeriod.
```

Это публичный starter contract практики «Cross-field validator». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `cross-field invariant` до запуска.

**B · Find the bug.** Найди нарушение `validation ordering` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Model validators за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Model validators и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Model validators?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Model validators: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный Junior answer

> Model validators — тема, в которой я сначала фиксирую `cross-field invariant`, затем объясняю `validation ordering` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и explicit null либо считать coercion бизнес-валидацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Model validators?**

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Expected answer rubric

### Must mention

- cross-field invariant
- validation ordering

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Model validators?

## Задача

### Cross-field validator

BookingPeriod(start,end) с model_validator: end строго больше start.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Model validators: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
