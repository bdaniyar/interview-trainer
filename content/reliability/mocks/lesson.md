# Mocking

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- объяснить `mock the boundary` своими словами и связать с backend-сценарием;
- объяснить `do not mock implementation details` своими словами и связать с backend-сценарием;
- объяснить `verify behavior carefully.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Тест подтверждает observable contract в изолированном сценарии; хорошие tests детерминированы и объясняют failure.

В теме **Mocking** важно уверенно объяснять следующие части:

### mock the boundary

Mock ставят в namespace использования и проверяют только значимое взаимодействие с внешней границей.

### do not mock implementation details

Mock ставят в namespace использования и проверяют только значимое взаимодействие с внешней границей.

### verify behavior carefully

Для `verify behavior carefully` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
import pytest

@pytest.mark.parametrize(("value", "expected"), [(0, False), (1, True)])
def test_is_positive(value, expected):
    assert is_positive(value) is expected
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Mock не в том namespace, shared fixture state или тест только happy path.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Mocking** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выдели unit boundary, integration boundary и критичный failure case. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- mock the boundary
- do not mock implementation details
- verify behavior carefully.
- Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Mock не в том namespace, shared fixture state или тест только happy path.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- mock the boundary
- do not mock implementation details
- verify behavior carefully.

## Задача

Разбери backend-сценарий: **Выдели unit boundary, integration boundary и критичный failure case.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Testing practice

### Mock boundary

**Сценарий:** Тест mock-ает private calls.

**Rubric:** Mock external boundary; assert outcome.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Mocking**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
