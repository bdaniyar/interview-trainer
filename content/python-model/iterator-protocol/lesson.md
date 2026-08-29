# Iterator protocol

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Iterator protocol**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``__iter__``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

The iterator protocol consists of `__iter__` returning an iterator and `__next__` returning an item or raising `StopIteration`.

### Как работает

A custom iterator stores its current position. A `for` loop calls `iter`, repeatedly calls `next` and catches `StopIteration` internally.


### Важный нюанс / limitation

`StopIteration` is a control signal for the protocol, not an ordinary error to print or broadly catch in consumer code.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `__iter__`
- `__next__`
- `StopIteration`
- custom iterator exercise

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Iterator protocol: отдельный пример

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print(list(Countdown(3)))
```

Iterator protocol состоит из `__iter__`, stateful `__next__` и `StopIteration`.

## Common mistakes

### Ошибка 1

Returning `None` instead of raising `StopIteration` creates an endless stream of None values instead of ending iteration.

## Practice

**A · Code/result prediction.** Change one input in the ``__iter__`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``__next__`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``__iter__`` and add one edge-case test.

**E · Interview explanation.** Explain Iterator protocol in 45–60 seconds and include one limitation.

## Code prediction

### Iterator исчерпывается

```python
it = iter([1, 2])
print(list(it), list(it))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1, 2] []
```

list потребил stateful iterator; повторный обход продолжается после его конца.

Misconception: `iterator-exhaustion`.

</details>

## Interview questions

### Основной вопрос

Что такое Iterator protocol и как это работает?

### Follow-up

Какая типичная ошибка связана с Iterator protocol?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

The iterator protocol consists of `__iter__` returning an iterator and `__next__` returning an item or raising `StopIteration`.

### Нормальный Junior answer

> The iterator protocol consists of `__iter__` returning an iterator and `__next__` returning an item or raising `StopIteration`. A custom iterator stores its current position. A `for` loop calls `iter`, repeatedly calls `next` and catches `StopIteration` internally. Важное ограничение: `StopIteration` is a control signal for the protocol, not an ordinary error to print or broadly catch in consumer code.

### Углубление / follow-up

**Какая типичная ошибка связана с Iterator protocol?**

Returning `None` instead of raising `StopIteration` creates an endless stream of None values instead of ending iteration.

## Expected answer rubric

### Must mention

- `__iter__`
- `__next__`
- `StopIteration`
- custom iterator exercise

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Returning `None` instead of raising `StopIteration` creates an endless stream of None values instead of ending iteration.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Iterator protocol?

## Задача

Сделай короткую письменную практику по теме **Iterator protocol**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** The iterator protocol consists of `__iter__` returning an iterator and `__next__` returning an item or raising `StopIteration`.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Returning `None` instead of raising `StopIteration` creates an endless stream of None values instead of ending iteration.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
