# Closures and free variables

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Closures and free variables**, а не только запомнить термин;
- прочитать и изменить короткий пример для `closure`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A closure is an inner function that retains access to free variables from its enclosing scope after the outer function returns.

### Как работает

The function stores references to enclosing cells, not a frozen copy of every value. A factory can therefore capture configuration or deliberately retain mutable state.


### Важный нюанс / limitation

Closures created in a loop exhibit late binding unless the current value is bound through a factory, default argument or `partial`.

### Где используется в backend

A validator or callback factory can capture immutable configuration without global state.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- closure
- enclosing scope
- free variable
- retained state

### Полезно

- practical factory/callback examples

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Closures and free variables: отдельный пример

```python
def make_prefixer(prefix):
    def render(value):
        return f"{prefix}:{value}"
    return render

user_key = make_prefixer("user")
print(user_key(42))
```

Closure продолжает видеть binding `prefix` после завершения внешней функции.

## Common mistakes

### Ошибка 1

Expecting each loop-created lambda to remember its loop iteration usually produces the final loop value for all callbacks.

## Practice

**A · Code/result prediction.** Change one input in the `closure` example and predict the result before running it.

**B · Find the bug.** Find code that violates `enclosing scope` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `closure` and add one edge-case test.

**E · Interview explanation.** Explain Closures and free variables in 45–60 seconds and include one limitation.

## Code prediction

### Closure хранит binding

```python
def make(prefix):
    def render(value):
        return f'{prefix}:{value}'
    return render
print(make('id')(7))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
id:7
```

Внутренняя функция замыкает свободное имя prefix после завершения make.

Misconception: `closure`.

</details>

## Interview questions

### Основной вопрос

Что такое Closures and free variables и как это работает?

### Follow-up

Какая типичная ошибка связана с Closures and free variables?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A closure is an inner function that retains access to free variables from its enclosing scope after the outer function returns.

### Нормальный Junior answer

> A closure is an inner function that retains access to free variables from its enclosing scope after the outer function returns. The function stores references to enclosing cells, not a frozen copy of every value. A factory can therefore capture configuration or deliberately retain mutable state. Важное ограничение: Closures created in a loop exhibit late binding unless the current value is bound through a factory, default argument or `partial`.

### Углубление / follow-up

**Какая типичная ошибка связана с Closures and free variables?**

Expecting each loop-created lambda to remember its loop iteration usually produces the final loop value for all callbacks.

## Expected answer rubric

### Must mention

- closure
- enclosing scope
- free variable
- retained state

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Expecting each loop-created lambda to remember its loop iteration usually produces the final loop value for all callbacks.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Closures and free variables?

## Задача

### Stateful closure

Верни next_value closure: начальное состояние start; каждый вызов увеличивает его на step и возвращает новое значение.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A closure is an inner function that retains access to free variables from its enclosing scope after the outer function returns.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Expecting each loop-created lambda to remember its loop iteration usually produces the final loop value for all callbacks.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
