# Serialization and `model_dump`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Serialization and `model_dump`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `JSON mode`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат.

**JSON mode.** `JSON mode` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.

**exclude unset.** `exclude unset` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.

**aliases.** `aliases` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.

**secret fields.** `secret fields` влияет на Pydantic v2 validation/serialization и должен различать missing, явное значение null, некорректные входные данные и представление результата.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `JSON mode` и `exclude unset` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `JSON mode`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- JSON mode
- exclude unset
- aliases
- secret fields

### Полезно

- связать Serialization and `model_dump` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Serialization and `model_dump`: отдельный пример

```python
def example_s15_serialization_and_model_dump() -> tuple[str, ...]:
    # Serialization and `model_dump`: проверяем отдельный contract урока.
    return ('JSON mode', 'exclude unset', 'aliases', 'secret fields',)

assert example_s15_serialization_and_model_dump()
```

Проверь missing, явное значение null, некорректные входные данные и serialized output Pydantic v2.

## Типичные ошибки

### Ошибка 1

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `JSON mode` до запуска.

**B · Найди ошибку.** Найди нарушение `exclude unset` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Serialization and `model_dump` за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Serialization and `model_dump` и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Serialization and `model_dump`: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный ответ уровня Junior

> Serialization and `model_dump` — тема, в которой я сначала фиксирую `JSON mode`, затем объясняю `exclude unset` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, явное значение null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?**

Смешать missing и явное значение null либо считать coercion бизнес-валидацией.

## Критерии хорошего ответа

### Что обязательно упомянуть

- JSON mode
- exclude unset
- aliases
- secret fields

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?

## Задача

Сделай короткую письменную практику по теме **Serialization and `model_dump`**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Serialization and `model_dump`: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и явное значение null либо считать coercion бизнес-валидацией.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
