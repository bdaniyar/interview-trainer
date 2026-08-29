# GIL

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; CPython details приоритетны только там, где объясняют реальные bugs.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **GIL**, а не только запомнить термин;
- прочитать и изменить короткий пример для `one thread executing Python bytecode in one CPython process`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

The CPython GIL allows one thread at a time to execute Python bytecode in a process.

### Как работает

Threads can still overlap waiting I/O because the GIL is released around many blocking/native operations. CPU-bound pure Python usually needs processes, native code that releases the GIL or external workers.


### Важный нюанс / limitation

The GIL is not an application lock: multi-step shared-state operations and database invariants still race.

## Mental model

Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- one thread executing Python bytecode in one CPython process
- threads still useful for I/O
- processes/native code for CPU work
- GIL is not a general lock for application data

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### GIL: отдельный пример

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Blocking I/O часто удобно отправить в threads.
with ThreadPoolExecutor(max_workers=4) as pool:
    io_results = list(pool.map(str.upper, ["a", "b"]))

# CPU-bound pure Python оценивают для processes, учитывая IPC.
print(io_results, ProcessPoolExecutor)
```

GIL не заменяет выбор workload: threads полезны для blocking I/O, processes обходят общий interpreter lock ценой IPC.

## Common mistakes

### Ошибка 1

Claiming that threads cannot race because of the GIL confuses bytecode scheduling with atomic business operations.

## Practice

**A · Code/result prediction.** Change one input in the `one thread executing Python bytecode in one CPython process` example and predict the result before running it.

**B · Find the bug.** Find code that violates `threads still useful for I/O` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `one thread executing Python bytecode in one CPython process` and add one edge-case test.

**E · Interview explanation.** Explain GIL in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое GIL и как это работает?

### Follow-up

Какая типичная ошибка связана с GIL?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

The CPython GIL allows one thread at a time to execute Python bytecode in a process.

### Нормальный Junior answer

> The CPython GIL allows one thread at a time to execute Python bytecode in a process. Threads can still overlap waiting I/O because the GIL is released around many blocking/native operations. CPU-bound pure Python usually needs processes, native code that releases the GIL or external workers. Важное ограничение: The GIL is not an application lock: multi-step shared-state operations and database invariants still race.

### Углубление / follow-up

**Какая типичная ошибка связана с GIL?**

Claiming that threads cannot race because of the GIL confuses bytecode scheduling with atomic business operations.

## Expected answer rubric

### Must mention

- one thread executing Python bytecode in one CPython process
- threads still useful for I/O
- processes/native code for CPU work
- GIL is not a general lock for application data

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Claiming that threads cannot race because of the GIL confuses bytecode scheduling with atomic business operations.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с GIL?

## Задача

Сделай короткую письменную практику по теме **GIL**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** The CPython GIL allows one thread at a time to execute Python bytecode in a process.
- **Механизм:** Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.
- **Ограничение:** Claiming that threads cannot race because of the GIL confuses bytecode scheduling with atomic business operations.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [gc](https://docs.python.org/3.12/library/gc.html)
- [threading](https://docs.python.org/3.12/library/threading.html)

Последняя проверка версий: **2026-08-27**.
