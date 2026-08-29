# Iterable vs iterator

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить `iterable` своими словами и связать с backend-сценарием;
- объяснить `iterator` своими словами и связать с backend-сценарием;
- объяснить ``iter`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **Iterable vs iterator** важно уверенно объяснять следующие части:

### iterable

Iterable умеет создать iterator через `__iter__`; один iterable может создавать новые независимые iterators для повторных обходов.

### iterator

Iterator возвращает себя из `__iter__` и сигнализирует завершение через `StopIteration`.

### `iter`

Для ``iter`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### `next`

Для ``next`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### single-pass state

Для `single-pass state` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### exhaustion

Для `exhaustion` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Iterable vs iterator** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- iterable
- iterator
- `iter`
- `next`
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

- iterable
- iterator
- `iter`
- `next`
- single-pass state
- exhaustion.

## Задача

### Лениво взять первый элемент

Верни первый элемент iterable либо default, не материализуя весь iterable.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Iterable vs iterator**;
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
