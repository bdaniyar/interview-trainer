# ThreadPoolExecutor

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Learning objectives

После урока ты сможешь:

- объяснить `wrapping blocking I/O` своими словами и связать с backend-сценарием;
- объяснить `bounded pool` своими словами и связать с backend-сценарием;
- объяснить `exception propagation.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Threads и processes решают разные задачи и имеют разную цену обмена состоянием.

В теме **ThreadPoolExecutor** важно уверенно объяснять следующие части:

### wrapping blocking I/O

Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

### bounded pool

Для `bounded pool` сравни shared memory, serialization, startup cost и подходящий I/O/CPU workload.

### exception propagation

Для `exception propagation` сравни shared memory, serialization, startup cost и подходящий I/O/CPU workload.

## Mental model

Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(read_remote_resource, urls))
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Отправлять непиклируемый объект в process pool или делить mutable state без lock.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **ThreadPoolExecutor** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери executor для I/O-bound и CPU-bound функций и объясни ограничения. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- wrapping blocking I/O
- bounded pool
- exception propagation.
- Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Отправлять непиклируемый объект в process pool или делить mutable state без lock.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- wrapping blocking I/O
- bounded pool
- exception propagation.

## Задача

Разбери backend-сценарий: **Выбери executor для I/O-bound и CPU-bound функций и объясни ограничения.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **ThreadPoolExecutor**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
