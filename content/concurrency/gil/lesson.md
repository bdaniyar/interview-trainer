# GIL

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; CPython details приоритетны только там, где объясняют реальные bugs.

## Learning objectives

После урока ты сможешь:

- объяснить `one thread executing Python bytecode in one CPython process` своими словами и связать с backend-сценарием;
- объяснить `threads still useful for I/O` своими словами и связать с backend-сценарием;
- объяснить `processes/native code for CPU work` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Детали CPython помогают объяснять lifetime, memory и ограничения потоков, но не заменяют измерения.

В теме **GIL** важно уверенно объяснять следующие части:

### one thread executing Python bytecode in one CPython process

Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

### threads still useful for I/O

Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management.

### processes/native code for CPU work

Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

### GIL is not a general lock for application data

CPython GIL допускает выполнение Python bytecode одним thread за раз, но отпускается вокруг части I/O/native calls и не защищает бизнес-инварианты от races.

## Mental model

Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

Сформулируй минимальный пример из текущего проекта: один happy path, одна граница и одна ошибка. Не добавляй инфраструктуру, не относящуюся к механизму.

## Common mistakes

**Ошибка:** Считать GIL автоматической защитой shared state или вызывать gc.collect как универсальную оптимизацию.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **GIL** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Классифицируй проблему как lifetime, allocation, race или CPU contention перед выбором инструмента. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- one thread executing Python bytecode in one CPython process
- threads still useful for I/O
- processes/native code for CPU work
- GIL is not a general lock for application data.
- Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Считать GIL автоматической защитой shared state или вызывать gc.collect как универсальную оптимизацию.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- one thread executing Python bytecode in one CPython process
- threads still useful for I/O
- processes/native code for CPU work
- GIL is not a general lock for application data.

## Задача

Разбери backend-сценарий: **Классифицируй проблему как lifetime, allocation, race или CPU contention перед выбором инструмента.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **GIL**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [gc](https://docs.python.org/3.12/library/gc.html)
- [threading](https://docs.python.org/3.12/library/threading.html)

Последняя проверка версий: **2026-08-27**.
