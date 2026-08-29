# Static hints vs runtime behavior

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Static hints vs runtime behavior**, а не только запомнить термин;
- прочитать и изменить короткий пример для `type hints`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Type hints describe contracts for static checkers, IDEs and readers; Python remains dynamically typed at runtime.

### Как работает

Annotations are stored as metadata and do not automatically insert type checks. Frameworks such as FastAPI/Pydantic explicitly inspect them to build validation/schema behavior.


### Важный нюанс / limitation

A passing type check is not input validation, and a runtime-valid coercion may still be undesirable for a domain rule.

### Где используется в backend

Typed service boundaries catch many mistakes before tests while Pydantic validates incoming request data.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- type hints
- static checker
- Python remains dynamic
- FastAPI/Pydantic use hints at runtime

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Static hints vs runtime behavior: отдельный пример

```python
def double(value: int) -> int:
    return value * 2

print(double(3))
print(double("a"))
```

Type checker отклонит второй вызов, но runtime Python выполнит operator строки без автоматической validation.

## Common mistakes

### Ошибка 1

Assuming `value: int` prevents a caller from passing a string leads to runtime surprises.

## Practice

**A · Code/result prediction.** Change one input in the `type hints` example and predict the result before running it.

**B · Find the bug.** Find code that violates `static checker` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `type hints` and add one edge-case test.

**E · Interview explanation.** Explain Static hints vs runtime behavior in 45–60 seconds and include one limitation.

## Code prediction

### Type hint не валидирует runtime

```python
def double(value: int) -> int:
    return value * 2
print(double('a'))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
aa
```

Обычная annotation не вставляет runtime type check; строка использует собственный operator *.

Misconception: `typing-runtime`.

</details>

## Interview questions

### Основной вопрос

Что такое Static hints vs runtime behavior и как это работает?

### Follow-up

Какая типичная ошибка связана с Static hints vs runtime behavior?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Type hints describe contracts for static checkers, IDEs and readers; Python remains dynamically typed at runtime.

### Нормальный Junior answer

> Type hints describe contracts for static checkers, IDEs and readers; Python remains dynamically typed at runtime. Annotations are stored as metadata and do not automatically insert type checks. Frameworks such as FastAPI/Pydantic explicitly inspect them to build validation/schema behavior. Важное ограничение: A passing type check is not input validation, and a runtime-valid coercion may still be undesirable for a domain rule.

### Углубление / follow-up

**Какая типичная ошибка связана с Static hints vs runtime behavior?**

Assuming `value: int` prevents a caller from passing a string leads to runtime surprises.

## Expected answer rubric

### Must mention

- type hints
- static checker
- Python remains dynamic
- FastAPI/Pydantic use hints at runtime

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Assuming `value: int` prevents a caller from passing a string leads to runtime surprises.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Static hints vs runtime behavior?

## Задача

Сделай короткую письменную практику по теме **Static hints vs runtime behavior**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Type hints describe contracts for static checkers, IDEs and readers; Python remains dynamically typed at runtime.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Assuming `value: int` prevents a caller from passing a string leads to runtime surprises.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
