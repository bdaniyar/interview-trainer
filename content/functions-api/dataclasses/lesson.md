# Dataclasses

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Dataclasses**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generated methods`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`@dataclass` generates methods such as `__init__`, `__repr__` and equality from declared fields.

### Как работает

Fields are processed in order; `field(default_factory=list)` creates a fresh mutable default per instance. `frozen=True` blocks normal field assignment but is not deep immutability.


### Важный нюанс / limitation

Dataclass is good for internal data/value objects; Pydantic handles untrusted validation and ORM models handle persistence.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`

### Полезно

- frozen
- domain data vs ORM/Pydantic models

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Dataclasses: отдельный пример

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class User:
    email: str
    roles: list[str] = field(default_factory=list)

a, b = User("a@example.com"), User("b@example.com")
a.roles.append("admin")
print(b.roles)
```

`default_factory` создаёт независимый mutable default для каждого dataclass instance.

## Common mistakes

### Ошибка 1

Using `items: list = []` is rejected/unsafe; mutable defaults need `default_factory`.

## Practice

**A · Code/result prediction.** Change one input in the `generated methods` example and predict the result before running it.

**B · Find the bug.** Find code that violates `equality/repr` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `generated methods` and add one edge-case test.

**E · Interview explanation.** Explain Dataclasses in 45–60 seconds and include one limitation.

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

## Interview questions

### Основной вопрос

Что такое Dataclasses и как это работает?

### Follow-up

Какая типичная ошибка связана с Dataclasses?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`@dataclass` generates methods such as `__init__`, `__repr__` and equality from declared fields.

### Нормальный Junior answer

> `@dataclass` generates methods such as `__init__`, `__repr__` and equality from declared fields. Fields are processed in order; `field(default_factory=list)` creates a fresh mutable default per instance. `frozen=True` blocks normal field assignment but is not deep immutability. Важное ограничение: Dataclass is good for internal data/value objects; Pydantic handles untrusted validation and ORM models handle persistence.

### Углубление / follow-up

**Какая типичная ошибка связана с Dataclasses?**

Using `items: list = []` is rejected/unsafe; mutable defaults need `default_factory`.

## Expected answer rubric

### Must mention

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using `items: list = []` is rejected/unsafe; mutable defaults need `default_factory`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Dataclasses?

## Задача

### Immutable BookingWindow

Создай frozen slots dataclass BookingWindow(start,end); end строго больше start; duration возвращает разницу.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `@dataclass` generates methods such as `__init__`, `__repr__` and equality from declared fields.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Using `items: list = []` is rejected/unsafe; mutable defaults need `default_factory`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
