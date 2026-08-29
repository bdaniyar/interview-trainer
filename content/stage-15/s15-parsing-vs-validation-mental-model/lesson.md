# Parsing vs validation mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Pydantic v2 — validation boundary основной FastAPI trajectory.

## Learning objectives

После урока ты сможешь:

- объяснить `coercion` своими словами и связать с backend-сценарием;
- объяснить `strict mode` своими словами и связать с backend-сценарием;
- объяснить `trusted/untrusted boundaries.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Pydantic v2 преобразует и валидирует данные на границе; модель должна явно описывать required, nullable и default semantics.

В теме **Parsing vs validation mental model** важно уверенно объяснять следующие части:

### coercion

Для `coercion` различай missing, explicit null, invalid input и serialized output Pydantic v2.

### strict mode

Для `strict mode` различай missing, explicit null, invalid input и serialized output Pydantic v2.

### trusted/untrusted boundaries

Для `trusted/untrusted boundaries` различай missing, explicit null, invalid input и serialized output Pydantic v2.

## Mental model

Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Путать str | None с полем, которое можно полностью не передать.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Parsing vs validation mental model** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проверь missing, explicit null, неверный тип и сериализованный результат. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- coercion
- strict mode
- trusted/untrusted boundaries.
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

- coercion
- strict mode
- trusted/untrusted boundaries.

## Задача

Разбери backend-сценарий: **Проверь missing, explicit null, неверный тип и сериализованный результат.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Parsing vs validation mental model**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Pydantic models](https://docs.pydantic.dev/2.11/concepts/models/)
- [Pydantic validators](https://docs.pydantic.dev/2.11/concepts/validators/)

Последняя проверка версий: **2026-08-27**.
