# Dataclasses

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- объяснить `generated methods` своими словами и связать с backend-сценарием;
- объяснить `equality/repr` своими словами и связать с backend-сценарием;
- объяснить `mutable fields` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

ООП в backend полезно как способ выразить состояние, поведение и границы ответственности, а не как соревнование по наследованию.

В теме **Dataclasses** важно уверенно объяснять следующие части:

### generated methods

Для `generated methods` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### equality/repr

Для `equality/repr` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### mutable fields

Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

### `field(default_factory=...)`

Для ``field(default_factory=...)`` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### frozen

Для `frozen` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### domain data vs ORM/Pydantic models

Для `domain data vs ORM/Pydantic models` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

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

1. Объясни **Dataclasses** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни composition и inheritance для сервиса уведомлений и назови цену изменения. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`
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

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`
- frozen
- domain data vs ORM/Pydantic models.

## Задача

### Immutable BookingWindow

Создай frozen slots dataclass BookingWindow(start,end); end строго больше start; duration возвращает разницу.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### dataclass equality

```python
from dataclasses import dataclass
@dataclass
class Point:
    x: int
print(Point(1) == Point(1), Point(1) is Point(1))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
True False
```

dataclass генерирует equality по полям, но каждый constructor call создаёт новый объект.

Misconception: `dataclass-equality`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Dataclasses**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
