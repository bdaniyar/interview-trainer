# Generator function and `yield`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Generator function and `yield`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generator object`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A generator function contains `yield`; calling it returns a generator object without running the body immediately.

### Как работает

Each `next` resumes execution until the next `yield`, preserving local variables and instruction position. Return or falling off the end raises `StopIteration` to the consumer.


### Важный нюанс / limitation

Laziness reduces peak memory but generators are single-use and defer exceptions until iteration reaches the failing line.

### Где используется в backend

Generators naturally stream rows or chunks instead of collecting the entire result in memory.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- generator object
- suspension/resume
- lazy evaluation
- generator state

### Полезно

- memory use

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Generator function and `yield`: отдельный пример

```python
def read_batches(rows, size):
    for start in range(0, len(rows), size):
        yield rows[start : start + size]

stream = read_batches([1, 2, 3, 4, 5], 2)
print(next(stream))
print(list(stream))
```

Generator сохраняет suspended frame между `yield` и лениво продолжает с текущей позиции.

## Common mistakes

### Ошибка 1

Converting a generator to list for logging before real use accidentally exhausts it.

## Practice

**A · Code/result prediction.** Change one input in the `generator object` example and predict the result before running it.

**B · Find the bug.** Find code that violates `suspension/resume` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `generator object` and add one edge-case test.

**E · Interview explanation.** Explain Generator function and `yield` in 45–60 seconds and include one limitation.

## Code prediction

### Generator ленивый

```python
def values():
    print('start')
    yield 1
g = values()
print('made')
print(next(g))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
made
start
1
```

Тело generator не выполняется при вызове функции, а стартует на первом next.

Misconception: `generator-laziness`.

</details>

### yield from передаёт значения

```python
def numbers():
    yield from [1, 2]
    yield 3
print(list(numbers()))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1, 2, 3]
```

yield from делегирует итерацию вложенному iterable до его исчерпания.

Misconception: `yield-from`.

</details>

## Interview questions

### Основной вопрос

Что такое Generator function and `yield` и как это работает?

### Follow-up

Какая типичная ошибка связана с Generator function and `yield`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A generator function contains `yield`; calling it returns a generator object without running the body immediately.

### Нормальный Junior answer

> A generator function contains `yield`; calling it returns a generator object without running the body immediately. Each `next` resumes execution until the next `yield`, preserving local variables and instruction position. Return or falling off the end raises `StopIteration` to the consumer. Важное ограничение: Laziness reduces peak memory but generators are single-use and defer exceptions until iteration reaches the failing line.

### Углубление / follow-up

**Какая типичная ошибка связана с Generator function and `yield`?**

Converting a generator to list for logging before real use accidentally exhausts it.

## Expected answer rubric

### Must mention

- generator object
- suspension/resume
- lazy evaluation
- generator state

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Converting a generator to list for logging before real use accidentally exhausts it.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Generator function and `yield`?

## Задача

Сделай короткую письменную практику по теме **Generator function and `yield`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A generator function contains `yield`; calling it returns a generator object without running the body immediately.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Converting a generator to list for logging before real use accidentally exhausts it.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
