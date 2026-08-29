# Parsing vs validation mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Parsing vs validation mental model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `coercion`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Как работает

Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат.

**coercion.** `coercion` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**strict mode.** `strict mode` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.

**trusted/untrusted boundaries.** `trusted/untrusted boundaries` влияет на Pydantic v2 validation/serialization и должен различать missing, explicit null, invalid input и output representation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `coercion` и `strict mode` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `coercion`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- coercion
- strict mode
- trusted/untrusted boundaries

### Полезно

- связать Parsing vs validation mental model с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Parsing vs validation mental model: отдельный пример

```python
def example_s15_parsing_vs_validation_mental_model() -> tuple[str, ...]:
    # Parsing vs validation mental model: проверяем отдельный contract урока.
    return ('coercion', 'strict mode', 'trusted/untrusted boundaries',)

assert example_s15_parsing_vs_validation_mental_model()
```

Проверь missing, explicit null, invalid input и serialized output Pydantic v2.

## Common mistakes

### Ошибка 1

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `coercion` до запуска.

**B · Find the bug.** Найди нарушение `strict mode` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Parsing vs validation mental model за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Parsing vs validation mental model и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Parsing vs validation mental model?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Parsing vs validation mental model: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.

### Нормальный Junior answer

> Parsing vs validation mental model — тема, в которой я сначала фиксирую `coercion`, затем объясняю `strict mode` на коротком примере. Ключевой механизм: Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат. Главная практическая ошибка — Смешать missing и explicit null либо считать coercion бизнес-валидацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Parsing vs validation mental model?**

Смешать missing и explicit null либо считать coercion бизнес-валидацией.

## Expected answer rubric

### Must mention

- coercion
- strict mode
- trusted/untrusted boundaries

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Parsing vs validation mental model?

## Задача

Сделай короткую письменную практику по теме **Parsing vs validation mental model**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Parsing vs validation mental model: Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.
- **Механизм:** Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.
- **Ограничение:** Смешать missing и explicit null либо считать coercion бизнес-валидацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
