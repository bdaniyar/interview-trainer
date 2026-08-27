# Test pyramid and test types

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- объяснить `unit` своими словами и связать с backend-сценарием;
- объяснить `integration` своими словами и связать с backend-сценарием;
- объяснить `end-to-end` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Тест подтверждает observable contract в изолированном сценарии; хорошие tests детерминированы и объясняют failure.

В теме **Test pyramid and test types** важно уверенно объяснять следующие части:

### unit

Для `unit` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

### integration

Для `integration` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

### end-to-end

Для `end-to-end` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

### contract awareness

Для `contract awareness` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

### correct boundary choice

Для `correct boundary choice` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.

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

1. Объясни **Test pyramid and test types** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выдели unit boundary, integration boundary и критичный failure case. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- unit
- integration
- end-to-end
- contract awareness
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

- unit
- integration
- end-to-end
- contract awareness
- correct boundary choice.

## Задача

Разбери backend-сценарий: **Выдели unit boundary, integration boundary и критичный failure case.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Testing practice

### Test boundary

**Сценарий:** Раздели booking flow на unit, integration и API tests.

**Rubric:** Unit domain decision; integration DB constraint; API status/body.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Test pyramid and test types**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
