# Generator function and `yield`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить `generator object` своими словами и связать с backend-сценарием;
- объяснить `suspension/resume` своими словами и связать с backend-сценарием;
- объяснить `lazy evaluation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Функция с `yield` возвращает generator object. Её выполнение приостанавливается между значениями, поэтому весь результат не нужно держать в памяти.

```python
def squares(limit):
    for value in range(limit):
        yield value ** 2
```

Генератор одноразовый: после исчерпания продолжить его нельзя. Для нового обхода вызови generator-функцию заново.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Generator function and `yield`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- generator object
- suspension/resume
- lazy evaluation
- generator state
- Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- generator object
- suspension/resume
- lazy evaluation
- generator state
- memory use.

## Задача

Реализуй генератор `batched(iterable, size)`, который лениво группирует элементы в списки размера `size`. Последняя группа может быть короче. При `size <= 0` подними `ValueError`.

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

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Generator function and `yield`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
