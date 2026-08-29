# Layered architecture

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Architecture basics нужны для объяснения design choices без senior-level overengineering.

## Learning objectives

После урока ты сможешь:

- объяснить `API` своими словами и связать с backend-сценарием;
- объяснить `service/use case` своими словами и связать с backend-сценарием;
- объяснить `data access` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Архитектура управляет зависимостями и стоимостью изменений; pattern полезен только при конкретной проблеме.

В теме **Layered architecture** важно уверенно объяснять следующие части:

### API

Для `API` проведи границу слоя и dependency direction, затем покажи test без реальной инфраструктуры.

### service/use case

Для `service/use case` проведи границу слоя и dependency direction, затем покажи test без реальной инфраструктуры.

### data access

Для `data access` проведи границу слоя и dependency direction, затем покажи test без реальной инфраструктуры.

### infrastructure

Для `infrastructure` проведи границу слоя и dependency direction, затем покажи test без реальной инфраструктуры.

## Mental model

Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Layered architecture: отдельный пример

```python
def example_s27_layered_architecture() -> tuple[str, ...]:
    # Layered architecture: проверяем отдельный contract урока.
    return ('API', 'service/use case', 'data access', 'infrastructure',)

assert example_s27_layered_architecture()
```

Проведи границу слоя и dependency direction; business rule не должен зависеть от framework.

## Common mistakes

**Ошибка:** Добавлять repository/service слои без поведения и тем самым создавать pass-through boilerplate.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Layered architecture** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови направление зависимости, seam для теста и ожидаемое изменение. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- API
- service/use case
- data access
- infrastructure.
- Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Добавлять repository/service слои без поведения и тем самым создавать pass-through boilerplate.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- API
- service/use case
- data access
- infrastructure.

## Задача

Разбери backend-сценарий: **Назови направление зависимости, seam для теста и ожидаемое изменение.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Layered architecture**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python abc](https://docs.python.org/3.12/library/abc.html)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
