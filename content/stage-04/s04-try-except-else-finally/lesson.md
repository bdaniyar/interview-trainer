# `try/except/else/finally`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`try/except/else/finally`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `control flow`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`try/except/else/finally` separates risky work, recovery, success-only work and unconditional cleanup.

### Как работает

`except` runs for a matching exception, `else` only when the try block succeeds, and `finally` runs before control leaves by success, return or exception.


### Важный нюанс / limitation

Keep the try block narrow so unrelated bugs are not mistaken for the expected failure.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- control flow
- cleanup
- return inside try/finally
- narrow exception scope

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### `try/except/else/finally`: отдельный пример

```python
def parse(value):
    try:
        result = int(value)
    except ValueError:
        return None
    else:
        return result
    finally:
        print("parse finished")

print(parse("7"))
```

`else` выполняется только без exception, `finally` — при любом пути выхода.

## Common mistakes

### Ошибка 1

A return inside finally overrides an earlier return or exception and can silently destroy diagnostic information.

## Practice

**A · Code/result prediction.** Change one input in the `control flow` example and predict the result before running it.

**B · Find the bug.** Find code that violates `cleanup` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `control flow` and add one edge-case test.

**E · Interview explanation.** Explain `try/except/else/finally` in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое `try/except/else/finally` и как это работает?

### Follow-up

Какая типичная ошибка связана с `try/except/else/finally`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`try/except/else/finally` separates risky work, recovery, success-only work and unconditional cleanup.

### Нормальный Junior answer

> `try/except/else/finally` separates risky work, recovery, success-only work and unconditional cleanup. `except` runs for a matching exception, `else` only when the try block succeeds, and `finally` runs before control leaves by success, return or exception. Важное ограничение: Keep the try block narrow so unrelated bugs are not mistaken for the expected failure.

### Углубление / follow-up

**Какая типичная ошибка связана с `try/except/else/finally`?**

A return inside finally overrides an earlier return or exception and can silently destroy diagnostic information.

## Expected answer rubric

### Must mention

- control flow
- cleanup
- return inside try/finally
- narrow exception scope

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- A return inside finally overrides an earlier return or exception and can silently destroy diagnostic information.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с `try/except/else/finally`?

## Задача

### Разобрать optional integer

None и пустая строка дают None; str/int преобразуются в int; bool и мусор дают ValueError с explicit cause.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `try/except/else/finally` separates risky work, recovery, success-only work and unconditional cleanup.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** A return inside finally overrides an earlier return or exception and can silently destroy diagnostic information.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
