# ThreadPoolExecutor

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **ThreadPoolExecutor**, а не только запомнить термин;
- прочитать и изменить короткий пример для `wrapping blocking I/O`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это модель выполнения работы с разной ценой shared memory, serialization и startup.

### Как работает

Определи workload: blocking I/O, CPU-bound Python или изолированная задача; затем оцени memory sharing и IPC.

**wrapping blocking I/O.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**bounded pool.** `bounded pool` определяет модель выполнения: threads делят память, processes используют isolation/serialization, а выбор зависит от I/O- или CPU-bound workload.

**exception propagation.** `exception propagation` определяет модель выполнения: threads делят память, processes используют isolation/serialization, а выбор зависит от I/O- или CPU-bound workload.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `wrapping blocking I/O` и `bounded pool` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- wrapping blocking I/O
- bounded pool
- exception propagation

### Полезно

- связать ThreadPoolExecutor с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### ThreadPoolExecutor: отдельный пример

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(url):
    return url.upper()

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(fetch, url) for url in ["/a", "/b"]]
    print([future.result() for future in as_completed(futures)])
```

Executor управляет bounded pool и Future objects; порядок `as_completed` зависит от завершения, не input.

## Common mistakes

### Ошибка 1

Разделить mutable state без synchronization или отправить несериализуемый object в process.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `wrapping blocking I/O` до запуска.

**B · Find the bug.** Найди нарушение `bounded pool` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про ThreadPoolExecutor за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое ThreadPoolExecutor и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

ThreadPoolExecutor: Это модель выполнения работы с разной ценой shared memory, serialization и startup.

### Нормальный Junior answer

> ThreadPoolExecutor — тема, в которой я сначала фиксирую `wrapping blocking I/O`, затем объясняю `bounded pool` на коротком примере. Ключевой механизм: Определи workload: blocking I/O, CPU-bound Python или изолированная задача; затем оцени memory sharing и IPC. Главная практическая ошибка — Разделить mutable state без synchronization или отправить несериализуемый object в process.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?**

Разделить mutable state без synchronization или отправить несериализуемый object в process.

## Expected answer rubric

### Must mention

- wrapping blocking I/O
- bounded pool
- exception propagation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Разделить mutable state без synchronization или отправить несериализуемый object в process.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?

## Задача

Сделай короткую письменную практику по теме **ThreadPoolExecutor**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** ThreadPoolExecutor: Это модель выполнения работы с разной ценой shared memory, serialization и startup.
- **Механизм:** Thread разделяет память процесса; process изолирован и требует сериализации/IPC.
- **Ограничение:** Разделить mutable state без synchronization или отправить несериализуемый object в process.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
