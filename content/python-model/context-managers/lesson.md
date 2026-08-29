# Context manager protocol

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Context manager protocol**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``with``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A context manager defines a reliable acquire/use/release boundary used by the `with` statement.

### Как работает

`__enter__` returns the value bound after `as`; `__exit__` receives exception information and cleanup runs even when the body fails. A truthy `__exit__` return suppresses the exception.


### Важный нюанс / limitation

Suppress only errors the context manager intentionally handles; returning True accidentally can hide real failures.

### Где используется в backend

Files, locks, DB transactions and clients use context managers to make resource lifetime visible.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `with`
- `__enter__`
- `__exit__`
- resource cleanup

### Полезно

- exception suppression

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Context manager protocol: отдельный пример

```python
class Transaction:
    def __enter__(self):
        print("begin")
        return self

    def __exit__(self, kind, value, traceback):
        print("rollback" if kind else "commit")
        return False

with Transaction():
    print("write")
```

Context manager централизует acquire/cleanup и не подавляет исключение при `False`.

## Common mistakes

### Ошибка 1

Manual open/close without finally leaks resources on an exception path.

## Practice

**A · Code/result prediction.** Change one input in the ``with`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``__enter__`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``with`` and add one edge-case test.

**E · Interview explanation.** Explain Context manager protocol in 45–60 seconds and include one limitation.

## Code prediction

### Context manager получает exception

```python
class Guard:
    def __enter__(self): return self
    def __exit__(self, kind, value, tb):
        print(kind.__name__)
        return True
with Guard():
    raise ValueError('x')
print('after')
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
ValueError
after
```

__exit__ получил тип ошибки и вернул True, поэтому исключение было подавлено.

Misconception: `context-manager-suppression`.

</details>

## Interview questions

### Основной вопрос

Что такое Context manager protocol и как это работает?

### Follow-up

Какая типичная ошибка связана с Context manager protocol?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A context manager defines a reliable acquire/use/release boundary used by the `with` statement.

### Нормальный Junior answer

> A context manager defines a reliable acquire/use/release boundary used by the `with` statement. `__enter__` returns the value bound after `as`; `__exit__` receives exception information and cleanup runs even when the body fails. A truthy `__exit__` return suppresses the exception. Важное ограничение: Suppress only errors the context manager intentionally handles; returning True accidentally can hide real failures.

### Углубление / follow-up

**Какая типичная ошибка связана с Context manager protocol?**

Manual open/close without finally leaks resources on an exception path.

## Expected answer rubric

### Must mention

- `with`
- `__enter__`
- `__exit__`
- resource cleanup

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Manual open/close without finally leaks resources on an exception path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Context manager protocol?

## Задача

### Transaction context manager

Создай Transaction: enter возвращает resource; success вызывает commit, error — rollback; исключение не подавляется.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A context manager defines a reliable acquire/use/release boundary used by the `with` statement.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Manual open/close without finally leaks resources on an exception path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
