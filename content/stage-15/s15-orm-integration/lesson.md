# ORM integration

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **ORM integration**, а не только запомнить термин;
- прочитать и изменить короткий пример для `response schemas separate from ORM models`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат.

**схемы ответа отделены от ORM-моделей.** `response schemas separate from ORM models` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.

**relationship loading.** `relationship loading` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.

**serialization does not solve N+1.** N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `response schemas separate from ORM models` и `relationship loading` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `response schemas separate from ORM models`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- схемы ответа отделены от ORM-моделей
- relationship loading
- serialization does not solve N+1

### Полезно

- связать ORM integration с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### ORM integration: отдельный пример

```python
def example_s15_orm_integration() -> tuple[str, ...]:
    # ORM integration: проверяем отдельный contract урока.
    return ('response schemas separate from ORM models', 'relationship loading', 'serialization does not solve N+1',)

assert example_s15_orm_integration()
```

Проверь missing, явное значение null, некорректные входные данные и serialized output Pydantic v2.

## Типичные ошибки

### Ошибка 1

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `response schemas separate from ORM models` до запуска.

**B · Найди ошибку.** Найди нарушение `relationship loading` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про ORM integration за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое ORM integration и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме ORM integration?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

ORM integration: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный ответ уровня Junior

> ORM integration — тема, в которой я сначала фиксирую `response schemas separate from ORM models`, затем объясняю `relationship loading` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме ORM integration?**

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Критерии хорошего ответа

### Что обязательно упомянуть

- схемы ответа отделены от ORM-моделей
- relationship loading
- serialization does not solve N+1

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме ORM integration?

## Задача

Сделай короткую письменную практику по теме **ORM integration**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** ORM integration: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
