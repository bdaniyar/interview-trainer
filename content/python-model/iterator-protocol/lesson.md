# Iterator protocol

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить ``__iter__`` своими словами и связать с backend-сценарием;
- объяснить ``__next__`` своими словами и связать с backend-сценарием;
- объяснить ``StopIteration`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Iterable возвращает iterator из `__iter__`. Iterator хранит состояние обхода, возвращает себя из `__iter__` и выдаёт элементы через `__next__`. Когда элементы закончились, он поднимает `StopIteration`.

```python
iterator = iter([10, 20])
next(iterator)  # 10
next(iterator)  # 20
```

Цикл `for` скрывает эти вызовы, но использует тот же протокол.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Iterator protocol** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `__iter__`
- `__next__`
- `StopIteration`
- custom iterator exercise.
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

- `__iter__`
- `__next__`
- `StopIteration`
- custom iterator exercise.

## Задача

Создай iterator-класс `Countdown(start)`, который выдаёт числа от `start` до `1`. После окончания каждый следующий `next()` должен поднимать `StopIteration`.

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

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Iterator protocol**;
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
