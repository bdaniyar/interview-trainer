# Rate limiting

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Rate limiting**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Redis shared atomic state`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Rate limiting** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Redis shared atomic state.** Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.

**fixed/sliding/token bucket trade-off.** `fixed/sliding/token bucket trade-off` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**multiple signals.** `multiple signals` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**fail policy depends on endpoint risk.** `fail policy depends on endpoint risk` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Redis shared atomic state` и `fixed/sliding/token bucket trade-off` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Redis shared atomic state`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Redis shared atomic state
- fixed/sliding/token bucket trade-off
- multiple signals
- fail policy depends on endpoint risk

### Полезно

- связать Rate limiting с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Rate limiting: отдельный пример

```text
Тема: Rate limiting

Фокус:
- Redis shared atomic state
- fixed/sliding/token bucket trade-off
- multiple signals
- fail policy depends on endpoint risk

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Redis shared atomic state` до запуска.

**B · Find the bug.** Найди нарушение `fixed/sliding/token bucket trade-off` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Rate limiting за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Rate limiting и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Rate limiting?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Rate limiting: это отдельный технический контракт

### Нормальный Junior answer

> Rate limiting — тема, в которой я сначала фиксирую `Redis shared atomic state`, затем объясняю `fixed/sliding/token bucket trade-off` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Rate limiting?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Redis shared atomic state
- fixed/sliding/token bucket trade-off
- multiple signals
- fail policy depends on endpoint risk

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Rate limiting?

## Задача

Сделай короткую письменную практику по теме **Rate limiting**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Rate limiting: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
