# Logs vs metrics vs traces

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.

## Learning objectives

После урока ты сможешь:

- объяснить `discrete events` своими словами и связать с backend-сценарием;
- объяснить `numeric time series` своими словами и связать с backend-сценарием;
- объяснить `request path across components.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Observability отвечает на вопросы о поведении системы через logs, metrics и traces.

В теме **Logs vs metrics vs traces** важно уверенно объяснять следующие части:

### discrete events

Для `discrete events` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### numeric time series

Для `numeric time series` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### request path across components

Для `request path across components` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

## Mental model

Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Логировать secrets или использовать user_id как Prometheus label.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Logs vs metrics vs traces** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: По росту p95 при стабильной средней выбери следующие metrics и logs. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- discrete events
- numeric time series
- request path across components.
- Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Логировать secrets или использовать user_id как Prometheus label.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- discrete events
- numeric time series
- request path across components.

## Задача

Разбери backend-сценарий: **По росту p95 при стабильной средней выбери следующие metrics и logs.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Logs vs metrics vs traces**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Prometheus concepts](https://prometheus.io/docs/concepts/)
- [Grafana fundamentals](https://grafana.com/docs/grafana/latest/fundamentals/)
- [Sentry concepts](https://docs.sentry.io/concepts/)

Последняя проверка версий: **2026-08-27**.
