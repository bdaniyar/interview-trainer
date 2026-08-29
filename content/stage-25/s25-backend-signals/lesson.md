# Backend signals

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.

## Learning objectives

После урока ты сможешь:

- объяснить `request rate` своими словами и связать с backend-сценарием;
- объяснить `error rate` своими словами и связать с backend-сценарием;
- объяснить `latency/p95` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Observability отвечает на вопросы о поведении системы через logs, metrics и traces.

В теме **Backend signals** важно уверенно объяснять следующие части:

### request rate

Для `request rate` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### error rate

Для `error rate` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### latency/p95

Для `latency/p95` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### DB errors

Для `DB errors` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### worker failures

Для `worker failures` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### queue backlog

Для `queue backlog` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.

### cache hit ratio where useful

`WHERE` фильтрует строки до grouping; SQL three-valued logic отбрасывает и `FALSE`, и `UNKNOWN`.

## Mental model

Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Backend signals: отдельный пример

```python
def example_s25_backend_signals() -> tuple[str, ...]:
    # Backend signals: проверяем отдельный contract урока.
    return ('request rate', 'error rate', 'latency/p95', 'DB errors',)

assert example_s25_backend_signals()
```

Сигнал полезен, когда содержит контекст, correlation и ведёт к конкретному действию.

## Common mistakes

**Ошибка:** Логировать secrets или использовать user_id как Prometheus label.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Backend signals** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: По росту p95 при стабильной средней выбери следующие metrics и logs. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- request rate
- error rate
- latency/p95
- DB errors
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

- request rate
- error rate
- latency/p95
- DB errors
- worker failures
- queue backlog
- cache hit ratio where useful.

## Задача

Разбери backend-сценарий: **По росту p95 при стабильной средней выбери следующие metrics и logs.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Backend signals**;
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
