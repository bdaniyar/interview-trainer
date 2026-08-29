# Exception hierarchy

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Exception hierarchy**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``BaseException``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Exceptions are objects in a hierarchy; application errors usually derive from `Exception`, while `BaseException` also includes process-control signals such as `KeyboardInterrupt`.

### Как работает

Python searches matching except clauses from top to bottom and unwinds stack frames until a handler is found; otherwise the traceback reaches the caller.


### Важный нюанс / limitation

Catch the narrow type you can handle. A broad catch must normally log context and re-raise rather than report false success.

### Где используется в backend

Domain exceptions can be translated to stable HTTP errors at the API boundary.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `BaseException`
- `Exception`
- common built-ins
- why not catch bare `except`

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Exception hierarchy: отдельный пример

```python
try:
    int("not-a-number")
except ValueError as exc:
    print(isinstance(exc, Exception))
    print(type(exc).__mro__[:3])
```

Иерархия позволяет перехватывать ожидаемый узкий тип, не скрывая системные и неожиданные ошибки.

## Common mistakes

### Ошибка 1

Bare `except:` can swallow cancellation or shutdown signals and hide programming bugs.

## Practice

**A · Code/result prediction.** Change one input in the ``BaseException`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``Exception`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``BaseException`` and add one edge-case test.

**E · Interview explanation.** Explain Exception hierarchy in 45–60 seconds and include one limitation.

## Code prediction

### finally выполняется при return

```python
def run():
    try:
        return 'result'
    finally:
        print('cleanup')
print(run())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
cleanup
result
```

Перед фактическим выходом из функции Python выполняет finally.

Misconception: `finally`.

</details>

## Debugging practice

### Broad exception

**Сценарий:** except Exception превращает DB outage в 404.

**Rubric:** Перехватывать ожидаемую domain error; unexpected log/re-raise.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Exception hierarchy и как это работает?

### Follow-up

Какая типичная ошибка связана с Exception hierarchy?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Exceptions are objects in a hierarchy; application errors usually derive from `Exception`, while `BaseException` also includes process-control signals such as `KeyboardInterrupt`.

### Нормальный Junior answer

> Exceptions are objects in a hierarchy; application errors usually derive from `Exception`, while `BaseException` also includes process-control signals such as `KeyboardInterrupt`. Python searches matching except clauses from top to bottom and unwinds stack frames until a handler is found; otherwise the traceback reaches the caller. Важное ограничение: Catch the narrow type you can handle. A broad catch must normally log context and re-raise rather than report false success.

### Углубление / follow-up

**Какая типичная ошибка связана с Exception hierarchy?**

Bare `except:` can swallow cancellation or shutdown signals and hide programming bugs.

## Expected answer rubric

### Must mention

- `BaseException`
- `Exception`
- common built-ins
- why not catch bare `except`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Bare `except:` can swallow cancellation or shutdown signals and hide programming bugs.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Exception hierarchy?

## Задача

Сделай короткую письменную практику по теме **Exception hierarchy**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Exceptions are objects in a hierarchy; application errors usually derive from `Exception`, while `BaseException` also includes process-control signals such as `KeyboardInterrupt`.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Bare `except:` can swallow cancellation or shutdown signals and hide programming bugs.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
