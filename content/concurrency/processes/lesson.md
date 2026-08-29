# Multiprocessing

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Multiprocessing**, а не только запомнить термин;
- прочитать и изменить короткий пример для `separate processes`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Multiprocessing runs work in separate processes with isolated memory and separate Python interpreters.

### Как работает

Inputs/results cross process boundaries through serialization and IPC. This enables CPU parallelism but adds startup, memory and communication cost.


### Важный нюанс / limitation

Worker targets and arguments generally must be pickleable, and process startup behavior differs by platform.

## Mental model

Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- separate processes
- serialization
- process startup/overhead
- CPU-bound work

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Multiprocessing: отдельный пример

```python
from multiprocessing import Process, Queue

def calculate(output):
    output.put(sum(value * value for value in range(10_000)))

queue = Queue()
process = Process(target=calculate, args=(queue,))
process.start(); process.join()
print(queue.get())
```

Process имеет отдельную память, поэтому результат передаётся через IPC, а arguments должны сериализоваться.

## Common mistakes

### Ошибка 1

Passing a live Session, lock-bound client or local closure to a process often fails serialization or creates invalid copied state.

## Practice

**A · Code/result prediction.** Change one input in the `separate processes` example and predict the result before running it.

**B · Find the bug.** Find code that violates `serialization` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `separate processes` and add one edge-case test.

**E · Interview explanation.** Explain Multiprocessing in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Multiprocessing и как это работает?

### Follow-up

Какая типичная ошибка связана с Multiprocessing?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Multiprocessing runs work in separate processes with isolated memory and separate Python interpreters.

### Нормальный Junior answer

> Multiprocessing runs work in separate processes with isolated memory and separate Python interpreters. Inputs/results cross process boundaries through serialization and IPC. This enables CPU parallelism but adds startup, memory and communication cost. Важное ограничение: Worker targets and arguments generally must be pickleable, and process startup behavior differs by platform.

### Углубление / follow-up

**Какая типичная ошибка связана с Multiprocessing?**

Passing a live Session, lock-bound client or local closure to a process often fails serialization or creates invalid copied state.

## Expected answer rubric

### Must mention

- separate processes
- serialization
- process startup/overhead
- CPU-bound work

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Passing a live Session, lock-bound client or local closure to a process often fails serialization or creates invalid copied state.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Multiprocessing?

## Задача

Сделай короткую письменную практику по теме **Multiprocessing**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Multiprocessing runs work in separate processes with isolated memory and separate Python interpreters.
- **Механизм:** Thread разделяет память процесса; process изолирован и требует сериализации/IPC.
- **Ограничение:** Passing a live Session, lock-bound client or local closure to a process often fails serialization or creates invalid copied state.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
