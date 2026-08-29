# Logs vs metrics vs traces

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Logs vs metrics vs traces**, а не только запомнить термин;
- прочитать и изменить короткий пример для `discrete events`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Logs vs metrics vs traces** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**discrete events.** `discrete events` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**numeric time series.** `numeric time series` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**request path across components.** `request path across components` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `discrete events` и `numeric time series` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `discrete events`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- discrete events
- numeric time series
- request path across components

### Полезно

- связать Logs vs metrics vs traces с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Logs vs metrics vs traces: отдельный пример

```python
def example_s25_logs_vs_metrics_vs_traces() -> tuple[str, ...]:
    # Logs vs metrics vs traces: проверяем отдельный contract урока.
    return ('discrete events', 'numeric time series', 'request path across components',)

assert example_s25_logs_vs_metrics_vs_traces()
```

Сигнал полезен, когда содержит контекст, correlation и ведёт к конкретному действию.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `discrete events` до запуска.

**B · Find the bug.** Найди нарушение `numeric time series` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Logs vs metrics vs traces за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Logs vs metrics vs traces и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Logs vs metrics vs traces?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Logs vs metrics vs traces: это отдельный технический контракт

### Нормальный Junior answer

> Logs vs metrics vs traces — тема, в которой я сначала фиксирую `discrete events`, затем объясняю `numeric time series` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Logs vs metrics vs traces?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- discrete events
- numeric time series
- request path across components

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Logs vs metrics vs traces?

## Задача

Сделай короткую письменную практику по теме **Logs vs metrics vs traces**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Logs vs metrics vs traces: это отдельный технический контракт
- **Механизм:** Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Prometheus concepts](https://prometheus.io/docs/concepts/)
- [Grafana fundamentals](https://grafana.com/docs/grafana/latest/fundamentals/)
- [Sentry concepts](https://docs.sentry.io/concepts/)

Последняя проверка версий: **2026-08-27**.
