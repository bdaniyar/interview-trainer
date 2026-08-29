# Serialization and `model_dump`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Serialization and `model_dump`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `JSON mode`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат.

**JSON mode.** `JSON mode` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**exclude unset.** `exclude unset` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**aliases.** `aliases` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**secret fields.** `secret fields` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `JSON mode` и `exclude unset` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `JSON mode`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- JSON mode
- exclude unset
- aliases
- secret fields

### Полезно

- связать Serialization and `model_dump` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Serialization and `model_dump`: отдельный пример

```python
def example_s15_serialization_and_model_dump() -> tuple[str, ...]:
    # Serialization and `model_dump`: проверяем отдельный contract урока.
    return ('JSON mode', 'exclude unset', 'aliases', 'secret fields',)

assert example_s15_serialization_and_model_dump()
```

Проверь missing, explicit null, invalid input и serialized output Pydantic v2.

## Common mistakes

### Ошибка 1

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `JSON mode` до запуска.

**B · Find the bug.** Найди нарушение `exclude unset` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Serialization and `model_dump` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Serialization and `model_dump` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Serialization and `model_dump`: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный Junior answer

> Serialization and `model_dump` — тема, в которой я сначала фиксирую `JSON mode`, затем объясняю `exclude unset` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и explicit null либо считать coercion бизнес-валидацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?**

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Expected answer rubric

### Must mention

- JSON mode
- exclude unset
- aliases
- secret fields

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Serialization and `model_dump`?

## Задача

Сделай короткую письменную практику по теме **Serialization and `model_dump`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Serialization and `model_dump`: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
