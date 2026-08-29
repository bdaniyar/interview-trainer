# Backend signals

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Backend signals**, а не только запомнить термин;
- прочитать и изменить короткий пример для `request rate`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Backend signals** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**request rate.** `request rate` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**error rate.** `error rate` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**latency/p95.** `latency/p95` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**DB errors.** `DB errors` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**worker failures.** `worker failures` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**queue backlog.** `queue backlog` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `request rate` и `error rate` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `request rate`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- request rate
- error rate
- latency/p95
- DB errors

### Полезно

- worker failures
- queue backlog

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

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

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `request rate` до запуска.

**B · Find the bug.** Найди нарушение `error rate` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Backend signals за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Backend signals и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Backend signals?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Backend signals: это отдельный технический контракт

### Нормальный Junior answer

> Backend signals — тема, в которой я сначала фиксирую `request rate`, затем объясняю `error rate` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Backend signals?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- request rate
- error rate
- latency/p95
- DB errors

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Backend signals?

## Задача

Сделай короткую письменную практику по теме **Backend signals**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Backend signals: это отдельный технический контракт
- **Механизм:** Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Prometheus concepts](https://prometheus.io/docs/concepts/)
- [Grafana fundamentals](https://grafana.com/docs/grafana/latest/fundamentals/)
- [Sentry concepts](https://docs.sentry.io/concepts/)

Последняя проверка версий: **2026-08-27**.
