# Threading

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Learning objectives

После урока ты сможешь:

- объяснить `shared process memory` своими словами и связать с backend-сценарием;
- объяснить `I/O-bound` своими словами и связать с backend-сценарием;
- объяснить `race conditions` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Threads и processes решают разные задачи и имеют разную цену обмена состоянием.

В теме **Threading** важно уверенно объяснять следующие части:

### shared process memory

Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

### I/O-bound

Для `I/O-bound` сравни shared memory, serialization, startup cost и подходящий I/O/CPU workload.

### race conditions

Для `race conditions` сравни shared memory, serialization, startup cost и подходящий I/O/CPU workload.

### locks

Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

### GIL limitations

CPython GIL допускает выполнение Python bytecode одним thread за раз, но отпускается вокруг части I/O/native calls и не защищает бизнес-инварианты от races.

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

1. Объясни **Threading** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери executor для I/O-bound и CPU-bound функций и объясни ограничения. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- shared process memory
- I/O-bound
- race conditions
- locks
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

- shared process memory
- I/O-bound
- race conditions
- locks
- GIL limitations.

## Задача

Разбери backend-сценарий: **Выбери executor для I/O-bound и CPU-bound функций и объясни ограничения.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Threads разделяют объект

```python
from threading import Thread
items = []
t = Thread(target=items.append, args=(1,))
t.start(); t.join()
print(items)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1]
```

Thread работает в памяти процесса; join гарантирует завершение перед print.

Misconception: `thread-shared-memory`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Threading**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
