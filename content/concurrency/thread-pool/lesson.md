# ThreadPoolExecutor

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **ThreadPoolExecutor**, а не только запомнить термин;
- прочитать и изменить короткий пример для `wrapping blocking I/O`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это модель выполнения работы с разной ценой shared memory, serialization и startup.

### Как работает

Определи workload: blocking I/O, CPU-bound Python или изолированная задача; затем оцени memory sharing и IPC.

**wrapping blocking I/O.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**bounded pool.** `bounded pool` определяет модель выполнения: threads делят память, processes используют isolation/serialization, а выбор зависит от I/O- или CPU-bound workload.

**exception propagation.** `exception propagation` определяет модель выполнения: threads делят память, processes используют isolation/serialization, а выбор зависит от I/O- или CPU-bound workload.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `wrapping blocking I/O` и `bounded pool` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Thread разделяет память процесса; process изолирован и требует сериализации/IPC.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- wrapping blocking I/O
- bounded pool
- exception propagation

### Полезно

- связать ThreadPoolExecutor с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Разделить mutable state без synchronization или отправить несериализуемый object в process.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `wrapping blocking I/O` до запуска.

**B · Найди ошибку.** Найди нарушение `bounded pool` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про ThreadPoolExecutor за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое ThreadPoolExecutor и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

ThreadPoolExecutor: Это модель выполнения работы с разной ценой shared memory, serialization и startup.

### Нормальный ответ уровня Junior

> ThreadPoolExecutor — тема, в которой я сначала фиксирую `wrapping blocking I/O`, затем объясняю `bounded pool` на коротком примере. Ключевой механизм: Определи workload: blocking I/O, CPU-bound Python или изолированная задача; затем оцени memory sharing и IPC. Главная практическая ошибка — Разделить mutable state без synchronization или отправить несериализуемый object в process.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?**

Разделить mutable state без synchronization или отправить несериализуемый object в process.

## Критерии хорошего ответа

### Что обязательно упомянуть

- wrapping blocking I/O
- bounded pool
- exception propagation

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Разделить mutable state без synchronization или отправить несериализуемый object в process.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме ThreadPoolExecutor?

## Задача

Сделай короткую письменную практику по теме **ThreadPoolExecutor**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** ThreadPoolExecutor: Это модель выполнения работы с разной ценой shared memory, serialization и startup.
- **Механизм:** Thread разделяет память процесса; process изолирован и требует сериализации/IPC.
- **Ограничение:** Разделить mutable state без synchronization или отправить несериализуемый object в process.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [concurrent.futures](https://docs.python.org/3.12/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3.12/library/multiprocessing.html)

Последняя проверка версий: **2026-08-27**.
