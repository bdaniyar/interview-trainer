# Iterable vs iterator

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Iterable vs iterator**, а не только запомнить термин;
- прочитать и изменить короткий пример для `iterable`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

An iterable can produce an iterator; an iterator is a stateful object that yields next values and is consumed.

### Как работает

`iter(obj)` obtains the iterator and `next(it)` asks for one item. A list can create a fresh iterator for each loop, while a generator object is typically its own single-pass iterator.


### Важный нюанс / limitation

After exhaustion, an iterator stays exhausted; call the iterable again to obtain a new traversal when supported.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- iterable
- iterator
- `iter`
- `next`

### Полезно

- single-pass state
- exhaustion

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Iterable vs iterator: отдельный пример

```python
numbers = [10, 20]
iterator = iter(numbers)

print(iter(numbers) is numbers)
print(iter(iterator) is iterator)
print(next(iterator))
```

List — iterable, создающий iterator; iterator хранит позицию и возвращает себя из `iter`.

## Common mistakes

### Ошибка 1

Storing one generator and iterating it twice gives an empty second pass, unlike iterating the original list twice.

## Practice

**A · Code/result prediction.** Change one input in the `iterable` example and predict the result before running it.

**B · Find the bug.** Find code that violates `iterator` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `iterable` and add one edge-case test.

**E · Interview explanation.** Explain Iterable vs iterator in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Iterable vs iterator и как это работает?

### Follow-up

Какая типичная ошибка связана с Iterable vs iterator?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

An iterable can produce an iterator; an iterator is a stateful object that yields next values and is consumed.

### Нормальный Junior answer

> An iterable can produce an iterator; an iterator is a stateful object that yields next values and is consumed. `iter(obj)` obtains the iterator and `next(it)` asks for one item. A list can create a fresh iterator for each loop, while a generator object is typically its own single-pass iterator. Важное ограничение: After exhaustion, an iterator stays exhausted; call the iterable again to obtain a new traversal when supported.

### Углубление / follow-up

**Какая типичная ошибка связана с Iterable vs iterator?**

Storing one generator and iterating it twice gives an empty second pass, unlike iterating the original list twice.

## Expected answer rubric

### Must mention

- iterable
- iterator
- `iter`
- `next`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Storing one generator and iterating it twice gives an empty second pass, unlike iterating the original list twice.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Iterable vs iterator?

## Задача

### Лениво взять первый элемент

Верни первый элемент iterable либо default, не материализуя весь iterable.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** An iterable can produce an iterator; an iterator is a stateful object that yields next values and is consumed.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Storing one generator and iterating it twice gives an empty second pass, unlike iterating the original list twice.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
