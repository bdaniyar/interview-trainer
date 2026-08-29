# Threading

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Threading**, а не только запомнить термин;
- прочитать и изменить короткий пример для `shared process memory`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A thread executes within one process and shares its memory, file descriptors and module state with other threads.

### Как работает

Threads are useful for blocking I/O libraries. Shared mutable state needs Lock or another synchronization design; `join` waits for completion.


### Важный нюанс / limitation

The GIL limits CPU-bound Python parallelism but does not prevent race conditions between multi-step operations.

## Mental model

Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- shared process memory
- I/O-bound
- race conditions
- locks

### Полезно

- GIL limitations

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Threading: отдельный пример

```python
from threading import Thread, current_thread

def work():
    print(current_thread().name)

thread = Thread(target=work, name="email-worker")
thread.start()
thread.join()
```

Thread разделяет память процесса; `join` задаёт явную точку ожидания завершения.

## Common mistakes

### Ошибка 1

Updating shared state with check-then-act logic without a lock can lose changes even when individual operations appear atomic.

## Practice

**A · Code/result prediction.** Change one input in the `shared process memory` example and predict the result before running it.

**B · Find the bug.** Find code that violates `I/O-bound` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `shared process memory` and add one edge-case test.

**E · Interview explanation.** Explain Threading in 45–60 seconds and include one limitation.

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

## Interview questions

### Основной вопрос

Что такое Threading и как это работает?

### Follow-up

Какая типичная ошибка связана с Threading?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A thread executes within one process and shares its memory, file descriptors and module state with other threads.

### Нормальный Junior answer

> A thread executes within one process and shares its memory, file descriptors and module state with other threads. Threads are useful for blocking I/O libraries. Shared mutable state needs Lock or another synchronization design; `join` waits for completion. Важное ограничение: The GIL limits CPU-bound Python parallelism but does not prevent race conditions between multi-step operations.

### Углубление / follow-up

**Какая типичная ошибка связана с Threading?**

Updating shared state with check-then-act logic without a lock can lose changes even when individual operations appear atomic.

## Expected answer rubric

### Must mention

- shared process memory
- I/O-bound
- race conditions
- locks

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Updating shared state with check-then-act logic without a lock can lose changes even when individual operations appear atomic.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Threading?

## Задача

Сделай короткую письменную практику по теме **Threading**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A thread executes within one process and shares its memory, file descriptors and module state with other threads.
- **Механизм:** Thread разделяет память процесса; process изолирован и требует сериализации/IPC.
- **Ограничение:** Updating shared state with check-then-act logic without a lock can lose changes even when individual operations appear atomic.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
