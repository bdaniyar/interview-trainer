# ORM integration

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **ORM integration**, а не только запомнить термин;
- прочитать и изменить короткий пример для `response schemas separate from ORM models`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат.

**response schemas separate from ORM models.** `response schemas separate from ORM models` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**relationship loading.** `relationship loading` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**serialization does not solve N+1.** N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `response schemas separate from ORM models` и `relationship loading` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `response schemas separate from ORM models`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- response schemas separate from ORM models
- relationship loading
- serialization does not solve N+1

### Полезно

- связать ORM integration с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### ORM integration: отдельный пример

```python
def example_s15_orm_integration() -> tuple[str, ...]:
    # ORM integration: проверяем отдельный contract урока.
    return ('response schemas separate from ORM models', 'relationship loading', 'serialization does not solve N+1',)

assert example_s15_orm_integration()
```

Проверь missing, explicit null, invalid input и serialized output Pydantic v2.

## Common mistakes

### Ошибка 1

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `response schemas separate from ORM models` до запуска.

**B · Find the bug.** Найди нарушение `relationship loading` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про ORM integration за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое ORM integration и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме ORM integration?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

ORM integration: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный Junior answer

> ORM integration — тема, в которой я сначала фиксирую `response schemas separate from ORM models`, затем объясняю `relationship loading` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и explicit null либо считать coercion бизнес-валидацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме ORM integration?**

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Expected answer rubric

### Must mention

- response schemas separate from ORM models
- relationship loading
- serialization does not solve N+1

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме ORM integration?

## Задача

Сделай короткую письменную практику по теме **ORM integration**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** ORM integration: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
