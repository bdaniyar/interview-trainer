# Generator expression vs list comprehension

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить `eager vs lazy` своими словами и связать с backend-сценарием;
- объяснить `single-use` своими словами и связать с backend-сценарием;
- объяснить `performance/memory` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **Generator expression vs list comprehension** важно уверенно объяснять следующие части:

### eager vs lazy

Для `eager vs lazy` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### single-use

Для `single-use` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### performance/memory

Для `performance/memory` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### when list is preferable

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Generator expression vs list comprehension: отдельный пример

```python
source = range(1_000_000)
lazy_squares = (value * value for value in source)
eager_squares = [value * value for value in range(3)]

print(next(lazy_squares))
print(eager_squares)
```

Generator expression вычисляет элементы по запросу; list comprehension сразу материализует результат.

## Common mistakes

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Generator expression vs list comprehension** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- eager vs lazy
- single-use
- performance/memory
- when list is preferable.
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

- eager vs lazy
- single-use
- performance/memory
- when list is preferable.

## Задача

Разбери backend-сценарий: **Покажи happy path, завершение протокола и поведение при исключении.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Generator expression vs list comprehension**;
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
