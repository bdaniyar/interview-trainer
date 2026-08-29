# Honest boundaries

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Honest boundaries**, а не только запомнить термин;
- прочитать и изменить короткий пример для `«Реализовал в pet-проекте; production traffic не заявляю».`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Honest boundaries** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**«Реализовал в pet-проекте; production traffic не заявляю».** `«Реализовал в pet-проекте; production traffic не заявляю»` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**«Могу объяснить failure modes и trade-offs».** `«Могу объяснить failure modes и trade-offs»` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**«Настраивал базовую интеграцию, но не управлял production cluster».** `«Настраивал базовую интеграцию, но не управлял production cluster»` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**«RabbitMQ/Kafka знаю концептуально, в проекте не использовал».** `«RabbitMQ/Kafka знаю концептуально, в проекте не использовал»` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**«DRF знаком на базовом уровне, основной практический стек — FastAPI».** `«DRF знаком на базовом уровне, основной практический стек — FastAPI»` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**“high-load” without measured traffic.** `“high-load” without measured traffic` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `«Реализовал в pet-проекте; production traffic не заявляю»` и `«Могу объяснить failure modes и trade-offs»` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `«Реализовал в pet-проекте; production traffic не заявляю»`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- «Реализовал в pet-проекте; production traffic не заявляю»
- «Могу объяснить failure modes и trade-offs»
- «Настраивал базовую интеграцию, но не управлял production cluster»
- «RabbitMQ/Kafka знаю концептуально, в проекте не использовал»

### Полезно

- «DRF знаком на базовом уровне, основной практический стек — FastAPI»
- “high-load” without measured traffic

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Honest boundaries: отдельный пример

```text
Сценарий: Спросили Kafka/Kubernetes/AWS.

Проверка:
Не заявлять опыт; learning plan; factual stack.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `«Реализовал в pet-проекте; production traffic не заявляю»` до запуска.

**B · Find the bug.** Найди нарушение `«Могу объяснить failure modes и trade-offs»` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Honest boundaries за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Honest boundary

**Сценарий:** Спросили Kafka/Kubernetes/AWS.

**Rubric:** Не заявлять опыт; learning plan; factual stack.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Honest boundaries и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Honest boundaries?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Honest boundaries: это отдельный технический контракт

### Нормальный Junior answer

> Honest boundaries — тема, в которой я сначала фиксирую `«Реализовал в pet-проекте; production traffic не заявляю»`, затем объясняю `«Могу объяснить failure modes и trade-offs»` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Honest boundaries?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- «Реализовал в pet-проекте; production traffic не заявляю»
- «Могу объяснить failure modes и trade-offs»
- «Настраивал базовую интеграцию, но не управлял production cluster»
- «RabbitMQ/Kafka знаю концептуально, в проекте не использовал»

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Honest boundaries?

## Задача

Сделай короткую письменную практику по теме **Honest boundaries**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Honest boundaries: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
