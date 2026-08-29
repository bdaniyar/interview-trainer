# Object, type, name and binding

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Object, type, name and binding**, а не только запомнить термин;
- прочитать и изменить короткий пример для `object`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Python name is a label in a namespace bound to an object; assignment binds a name and normally does not copy the object.

### Как работает

Each object has a type, identity and value. `a = b` makes both names refer to the same object; later rebinding `a = ...` changes only name `a`, while mutation is visible through every alias.


### Важный нюанс / limitation

Function arguments use the same object-reference model: a function can mutate a passed list, but rebinding its local parameter does not rebind the caller's name.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- object
- type
- name
- binding

### Полезно

- переменная как имя, связанное с объектом
- assignment не копирует объект

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Object, type, name and binding: отдельный пример

```python
message = "Learn with Pythoria"
alias = message

print(type(message).__name__)
print(message is alias)

alias = alias.upper()
print(message, alias)
```

Имена `message` и `alias` сначала связаны с одним `str`; новый assignment переводит только `alias` на новый объект.

## Common mistakes

### Ошибка 1

Treating a variable as an independent box leads to wrong predictions for aliases and function arguments.

## Practice

**A · Code/result prediction.** Change one input in the `object` example and predict the result before running it.

**B · Find the bug.** Find code that violates `type` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `object` and add one edge-case test.

**E · Interview explanation.** Explain Object, type, name and binding in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Object, type, name and binding и как это работает?

### Follow-up

Какая типичная ошибка связана с Object, type, name and binding?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Python name is a label in a namespace bound to an object; assignment binds a name and normally does not copy the object.

### Нормальный Junior answer

> Python name is a label in a namespace bound to an object; assignment binds a name and normally does not copy the object. Each object has a type, identity and value. `a = b` makes both names refer to the same object; later rebinding `a = ...` changes only name `a`, while mutation is visible through every alias. Важное ограничение: Function arguments use the same object-reference model: a function can mutate a passed list, but rebinding its local parameter does not rebind the caller's name.

### Углубление / follow-up

**Какая типичная ошибка связана с Object, type, name and binding?**

Treating a variable as an independent box leads to wrong predictions for aliases and function arguments.

## Expected answer rubric

### Must mention

- object
- type
- name
- binding

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Treating a variable as an independent box leads to wrong predictions for aliases and function arguments.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Object, type, name and binding?

## Задача

Сделай короткую письменную практику по теме **Object, type, name and binding**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Python name is a label in a namespace bound to an object; assignment binds a name and normally does not copy the object.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Treating a variable as an independent box leads to wrong predictions for aliases and function arguments.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
