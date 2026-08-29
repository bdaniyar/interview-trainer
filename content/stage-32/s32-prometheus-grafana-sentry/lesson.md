# Prometheus/Grafana/Sentry

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Prometheus/Grafana/Sentry**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Prometheus collects time-series metrics`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Prometheus/Grafana/Sentry** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Prometheus collects time-series metrics.** `Prometheus collects time-series metrics` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**Grafana visualizes data and dashboards.** `Grafana visualizes data and dashboards` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**Sentry groups application errors with stack/context.** GROUP BY формирует группы до вычисления aggregates, а HAVING фильтрует уже агрегированные группы.

**candidate configured and used them in a pet-project.** `candidate configured and used them in a pet-project` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**candidate did not administer a production monitoring cluster.** `candidate did not administer a production monitoring cluster` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Prometheus collects time-series metrics` и `Grafana visualizes data and dashboards` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Prometheus collects time-series metrics`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Prometheus collects time-series metrics
- Grafana visualizes data and dashboards
- Sentry groups application errors with stack/context
- candidate configured and used them in a pet-project

### Полезно

- candidate did not administer a production monitoring cluster

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Prometheus/Grafana/Sentry: отдельный пример

```text
Тема: Prometheus/Grafana/Sentry

Фокус:
- Prometheus collects time-series metrics
- Grafana visualizes data and dashboards
- Sentry groups application errors with stack/context
- candidate configured and used them in a pet-project

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Prometheus collects time-series metrics` до запуска.

**B · Find the bug.** Найди нарушение `Grafana visualizes data and dashboards` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Prometheus/Grafana/Sentry за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Prometheus/Grafana/Sentry и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Prometheus/Grafana/Sentry?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Prometheus/Grafana/Sentry: это отдельный технический контракт

### Нормальный Junior answer

> Prometheus/Grafana/Sentry — тема, в которой я сначала фиксирую `Prometheus collects time-series metrics`, затем объясняю `Grafana visualizes data and dashboards` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Prometheus/Grafana/Sentry?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Prometheus collects time-series metrics
- Grafana visualizes data and dashboards
- Sentry groups application errors with stack/context
- candidate configured and used them in a pet-project

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Prometheus/Grafana/Sentry?

## Задача

Сделай короткую письменную практику по теме **Prometheus/Grafana/Sentry**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Prometheus/Grafana/Sentry: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
