# Binary search

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.

## Learning objectives

После урока ты сможешь:

- объяснить `sorted invariant` своими словами и связать с backend-сценарием;
- объяснить `boundaries` своими словами и связать с backend-сценарием;
- объяснить `O(log n).` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Для Junior backend важны базовые структуры и сложность реальных transformations, а не редкие олимпиадные трюки.

В теме **Binary search** важно уверенно объяснять следующие части:

### sorted invariant

Для `sorted invariant` назови input constraints, data structure, complexity и boundary cases до написания кода.

### boundaries

Для `boundaries` назови input constraints, data structure, complexity и boundary cases до написания кода.

### O(log n)

Для `O(log n)` назови input constraints, data structure, complexity и boundary cases до написания кода.

## Mental model

Выбери структуру по операциям и оцени dominant time/space term.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Binary search: отдельный пример

```python
from collections import Counter
counts = Counter('aba')
print(counts['a'], counts['x'])
```

Expected: `2 0`. Counter возвращает ноль для отсутствующего ключа вместо KeyError.

## Common mistakes

**Ошибка:** Писать O(n²), когда один dict даёт линейный проход, или оптимизировать без constraints.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Binary search** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Реши задачу сначала корректно, затем назови complexity и граничные случаи. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- sorted invariant
- boundaries
- O(log n).
- Выбери структуру по операциям и оцени dominant time/space term.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Писать O(n²), когда один dict даёт линейный проход, или оптимизировать без constraints.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- sorted invariant
- boundaries
- O(log n).

## Задача

Разбери backend-сценарий: **Реши задачу сначала корректно, затем назови complexity и граничные случаи.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Счётчик частот

```python
from collections import Counter
counts = Counter('aba')
print(counts['a'], counts['x'])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
2 0
```

Counter возвращает ноль для отсутствующего ключа вместо KeyError.

Misconception: `counter`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Binary search**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python collections](https://docs.python.org/3.12/library/collections.html)
- [Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)

Последняя проверка версий: **2026-08-27**.
