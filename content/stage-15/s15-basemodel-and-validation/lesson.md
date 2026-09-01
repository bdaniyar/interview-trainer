# BaseModel and validation

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **BaseModel and validation**, а не только запомнить термин;
- прочитать и изменить короткий пример для `BaseModel and validation`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат.

**BaseModel and validation.** Pydantic `BaseModel` превращает недоверенный input в типизированный объект по core schema; validation errors относятся к границе входа, не бизнес-правилам.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `BaseModel and validation` и `BaseModel and validation` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `BaseModel and validation`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- BaseModel and validation

### Полезно

- связать BaseModel and validation с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### BaseModel and validation: отдельный пример

```python
from pydantic import BaseModel

# Создай UserCreate.
```

Это публичный starter contract практики «UserCreate model». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `BaseModel and validation` до запуска.

**B · Найди ошибку.** Найди нарушение `BaseModel and validation` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про BaseModel and validation за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое BaseModel and validation и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме BaseModel and validation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

BaseModel and validation: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный ответ уровня Junior

> BaseModel and validation — тема, в которой я сначала фиксирую `BaseModel and validation`, затем объясняю `BaseModel and validation` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме BaseModel and validation?**

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Критерии хорошего ответа

### Что обязательно упомянуть

- BaseModel and validation

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме BaseModel and validation?

## Задача

### UserCreate model

Pydantic UserCreate: username min_length=3, age 14..120.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** BaseModel and validation: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
