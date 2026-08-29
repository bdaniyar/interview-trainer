# LEGB

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **LEGB**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Local`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

LEGB is Python's name lookup order: Local, Enclosing, Global, Builtins.

### Как работает

A read searches those scopes in order. Assignment inside a function makes the name local unless declared `global` or `nonlocal`, which can cause `UnboundLocalError` when the name is read before local assignment.


### Важный нюанс / limitation

Shadowing `list`, `id` or another builtin works but makes later calls confusing or broken.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Local
- Enclosing
- Global
- Builtins

### Полезно

- name lookup
- shadowing

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### LEGB: отдельный пример

```python
label = "global"

def outer():
    label = "enclosing"
    def inner():
        label = "local"
        return label
    return inner(), label

print(outer(), label)
```

Три разных bindings с одним именем находятся на local, enclosing и global уровнях.

## Common mistakes

### Ошибка 1

Assuming assignment updates a global while Python created a new local binding causes wrong state and `UnboundLocalError`.

## Practice

**A · Code/result prediction.** Change one input in the `Local` example and predict the result before running it.

**B · Find the bug.** Find code that violates `Enclosing` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `Local` and add one edge-case test.

**E · Interview explanation.** Explain LEGB in 45–60 seconds and include one limitation.

## Code prediction

### LEGB и локальное имя

```python
value = 'global'
def read():
    value = 'local'
    return value
print(read(), value)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
local global
```

Assignment внутри функции создаёт local binding и не меняет global binding.

Misconception: `legb`.

</details>

## Interview questions

### Основной вопрос

Что такое LEGB и как это работает?

### Follow-up

Какая типичная ошибка связана с LEGB?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

LEGB is Python's name lookup order: Local, Enclosing, Global, Builtins.

### Нормальный Junior answer

> LEGB is Python's name lookup order: Local, Enclosing, Global, Builtins. A read searches those scopes in order. Assignment inside a function makes the name local unless declared `global` or `nonlocal`, which can cause `UnboundLocalError` when the name is read before local assignment. Важное ограничение: Shadowing `list`, `id` or another builtin works but makes later calls confusing or broken.

### Углубление / follow-up

**Какая типичная ошибка связана с LEGB?**

Assuming assignment updates a global while Python created a new local binding causes wrong state and `UnboundLocalError`.

## Expected answer rubric

### Must mention

- Local
- Enclosing
- Global
- Builtins

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Assuming assignment updates a global while Python created a new local binding causes wrong state and `UnboundLocalError`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с LEGB?

## Задача

Сделай короткую письменную практику по теме **LEGB**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** LEGB is Python's name lookup order: Local, Enclosing, Global, Builtins.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Assuming assignment updates a global while Python created a new local binding causes wrong state and `UnboundLocalError`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
