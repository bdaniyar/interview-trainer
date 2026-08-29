# Mutability and immutability

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Mutability and immutability**, а не только запомнить термин;
- прочитать и изменить короткий пример для `mutable/immutable`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Mutable objects can change while keeping identity; immutable objects cannot be changed in place and an apparent update creates or binds another object.

### Как работает

Lists, dicts and sets expose mutating operations. Integers, strings, bytes and tuples do not. A tuple itself is immutable but may contain a mutable element.


### Важный нюанс / limitation

Mutability matters more than the syntax: `name += value` may mutate a list but creates a new string object.

### Где используется в backend

Shared mutable request/config defaults can leak state between calls.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- mutable/immutable
- mutation vs rebinding
- list, dict, set
- int, str, bytes, tuple

### Полезно

- tuple с mutable element
- effect on function arguments

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Mutability and immutability: отдельный пример

```python
roles = ["reader"]
original_id = id(roles)
roles.append("writer")

name = "api"
old_name_id = id(name)
name += "-v2"

print(id(roles) == original_id)
print(id(name) == old_name_id)
```

List меняется с сохранением identity; операция со строкой создаёт новый immutable объект.

## Common mistakes

### Ошибка 1

Confusing mutation with rebinding makes a caller's data change unexpectedly through an alias.

## Practice

**A · Code/result prediction.** Change one input in the `mutable/immutable` example and predict the result before running it.

**B · Find the bug.** Find code that violates `mutation vs rebinding` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `mutable/immutable` and add one edge-case test.

**E · Interview explanation.** Explain Mutability and immutability in 45–60 seconds and include one limitation.

## Code prediction

### Два имени одного списка

```python
a = []
b = a
b.append(1)
print(a)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1]
```

Assignment связал b с тем же mutable list; append виден через оба имени.

Misconception: `aliasing`.

</details>

## Interview questions

### Основной вопрос

Что такое Mutability and immutability и как это работает?

### Follow-up

Какая типичная ошибка связана с Mutability and immutability?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Mutable objects can change while keeping identity; immutable objects cannot be changed in place and an apparent update creates or binds another object.

### Нормальный Junior answer

> Mutable objects can change while keeping identity; immutable objects cannot be changed in place and an apparent update creates or binds another object. Lists, dicts and sets expose mutating operations. Integers, strings, bytes and tuples do not. A tuple itself is immutable but may contain a mutable element. Важное ограничение: Mutability matters more than the syntax: `name += value` may mutate a list but creates a new string object.

### Углубление / follow-up

**Какая типичная ошибка связана с Mutability and immutability?**

Confusing mutation with rebinding makes a caller's data change unexpectedly through an alias.

## Expected answer rubric

### Must mention

- mutable/immutable
- mutation vs rebinding
- list, dict, set
- int, str, bytes, tuple

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Confusing mutation with rebinding makes a caller's data change unexpectedly through an alias.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Mutability and immutability?

## Задача

Сделай короткую письменную практику по теме **Mutability and immutability**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Mutable objects can change while keeping identity; immutable objects cannot be changed in place and an apparent update creates or binds another object.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Confusing mutation with rebinding makes a caller's data change unexpectedly through an alias.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
