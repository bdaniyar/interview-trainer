# Sync vs async endpoints

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Sync vs async endpoints**, а не только запомнить термин;
- прочитать и изменить короткий пример для `threadpool behavior for sync endpoint`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

FastAPI поддерживает sync и async endpoints; async полезен, когда весь dependency stack выполняет awaitable I/O.

### Как работает

Async endpoint работает на event loop, а sync endpoint обычно отправляется в thread pool, чтобы blocking work не останавливал loop напрямую.


### Важный нюанс / ограничение

`async def` не превращает sync driver в неблокирующий: нужен async driver/client или явный offload.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- поведение пула потоков для синхронного эндпоинта
- blocking inside async
- асинхронность нужна, только когда от неё выигрывает весь стек зависимостей

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Sync vs async endpoints: отдельный пример

```text
Сценарий: Async route вызывает sync dependency с долгим blocking client внутри event loop.

Проверка:
Использовать async client/driver или thread offload; измерить event-loop lag и concurrent latency.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

`requests` или sync DB driver внутри async endpoint блокирует loop несмотря на объявление async function.

## Практика

**A · Предсказание результата.** Измени один input в примере `threadpool behavior for sync endpoint` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `blocking inside async`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `threadpool behavior for sync endpoint`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Sync vs async endpoints за 45–60 секунд и назови одно ограничение.

## Практика: Отладка

### Blocking dependency

**Сценарий:** Async route вызывает sync dependency с долгим blocking client внутри event loop.

**Критерии ответа:** Использовать async client/driver или thread offload; измерить event-loop lag и concurrent latency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Sync vs async endpoints и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Sync vs async endpoints?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

FastAPI поддерживает sync и async endpoints; async полезен, когда весь dependency stack выполняет awaitable I/O.

### Нормальный ответ уровня Junior

> FastAPI поддерживает sync и async endpoints; async полезен, когда весь dependency stack выполняет awaitable I/O. Async endpoint работает на event loop, а sync endpoint обычно отправляется в thread pool, чтобы blocking work не останавливал loop напрямую. Важное ограничение: `async def` не превращает sync driver в неблокирующий: нужен async driver/client или явный offload.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Sync vs async endpoints?**

`requests` или sync DB driver внутри async endpoint блокирует loop несмотря на объявление async function.

## Критерии хорошего ответа

### Что обязательно упомянуть

- поведение пула потоков для синхронного эндпоинта
- blocking inside async
- асинхронность нужна, только когда от неё выигрывает весь стек зависимостей

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- `requests` или sync DB driver внутри async endpoint блокирует loop несмотря на объявление async function.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Sync vs async endpoints?

## Задача

Сделай короткую письменную практику по теме **Sync vs async endpoints**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** FastAPI поддерживает sync и async endpoints; async полезен, когда весь dependency stack выполняет awaitable I/O.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** `requests` или sync DB driver внутри async endpoint блокирует loop несмотря на объявление async function.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
