# Class, instance and attributes

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Class, instance and attributes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `class object`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A class is an object describing behavior and class attributes; an instance has its own identity and instance namespace.

### Как работает

Attribute lookup starts on the instance, then follows the class MRO; methods found on the class become bound methods when read through an instance.


### Важный нюанс / limitation

A mutable class attribute is shared by instances until an instance shadows the name.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- class object
- instance
- instance namespace
- class namespace

### Полезно

- attribute lookup

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Class, instance and attributes: отдельный пример

```python
class User:
    kind = "account"

    def __init__(self, email):
        self.email = email

user = User("a@example.com")
print(user.email, user.kind, type(user).__name__)
```

Instance хранит собственный `email`, а attribute lookup находит общий `kind` в class.

## Common mistakes

### Ошибка 1

Defining `items = []` on the class for per-instance data leaks mutations between all instances.

## Practice

**A · Code/result prediction.** Change one input in the `class object` example and predict the result before running it.

**B · Find the bug.** Find code that violates `instance` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `class object` and add one edge-case test.

**E · Interview explanation.** Explain Class, instance and attributes in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Class, instance and attributes и как это работает?

### Follow-up

Какая типичная ошибка связана с Class, instance and attributes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A class is an object describing behavior and class attributes; an instance has its own identity and instance namespace.

### Нормальный Junior answer

> A class is an object describing behavior and class attributes; an instance has its own identity and instance namespace. Attribute lookup starts on the instance, then follows the class MRO; methods found on the class become bound methods when read through an instance. Важное ограничение: A mutable class attribute is shared by instances until an instance shadows the name.

### Углубление / follow-up

**Какая типичная ошибка связана с Class, instance and attributes?**

Defining `items = []` on the class for per-instance data leaks mutations between all instances.

## Expected answer rubric

### Must mention

- class object
- instance
- instance namespace
- class namespace

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Defining `items = []` on the class for per-instance data leaks mutations between all instances.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Class, instance and attributes?

## Задача

Сделай короткую письменную практику по теме **Class, instance and attributes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A class is an object describing behavior and class attributes; an instance has its own identity and instance namespace.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Defining `items = []` on the class for per-instance data leaks mutations between all instances.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
