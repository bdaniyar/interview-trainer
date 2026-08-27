# MRO and multiple inheritance

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- объяснить `C3 linearization intuition` своими словами и связать с backend-сценарием;
- объяснить ``Class.__mro__`` своими словами и связать с backend-сценарием;
- объяснить `diamond problem` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

ООП в backend полезно как способ выразить состояние, поведение и границы ответственности, а не как соревнование по наследованию.

В теме **MRO and multiple inheritance** важно уверенно объяснять следующие части:

### C3 linearization intuition

Для `C3 linearization intuition` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### `Class.__mro__`

MRO задаёт детерминированный порядок поиска атрибутов при multiple inheritance; `super()` продолжает поиск по MRO фактического класса.

### diamond problem

Для `diamond problem` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### cooperative `super`

Для `cooperative `super`` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### common interview predictions

`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UserId:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("user id must be positive")
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Создавать глубокую иерархию ради переиспользования нескольких строк.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **MRO and multiple inheritance** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни composition и inheritance для сервиса уведомлений и назови цену изменения. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- C3 linearization intuition
- `Class.__mro__`
- diamond problem
- cooperative `super`
- У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Создавать глубокую иерархию ради переиспользования нескольких строк.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- C3 linearization intuition
- `Class.__mro__`
- diamond problem
- cooperative `super`
- common interview predictions.

## Задача

Разбери backend-сценарий: **Сравни composition и inheritance для сервиса уведомлений и назови цену изменения.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **MRO and multiple inheritance**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
