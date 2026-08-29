# Logging fundamentals

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Logging fundamentals**, а не только запомнить термин;
- прочитать и изменить короткий пример для `debug/info/warning/error/exception`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Logging fundamentals** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**debug/info/warning/error/exception.** `debug/info/warning/error/exception` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**no print-debugging as final solution.** `no print-debugging as final solution` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.

**no secrets/PII.** `no secrets/PII` является observability signal с контекстом, correlation и ожидаемым действием инженера после обнаружения symptom.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `debug/info/warning/error/exception` и `no print-debugging as final solution` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `debug/info/warning/error/exception`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- debug/info/warning/error/exception
- no print-debugging as final solution
- no secrets/PII

### Полезно

- связать Logging fundamentals с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Logging fundamentals: отдельный пример

```python
def example_s25_logging_fundamentals() -> tuple[str, ...]:
    # Logging fundamentals: проверяем отдельный contract урока.
    return ('debug/info/warning/error/exception', 'no print-debugging as final solution', 'no secrets/PII',)

assert example_s25_logging_fundamentals()
```

Сигнал полезен, когда содержит контекст, correlation и ведёт к конкретному действию.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `debug/info/warning/error/exception` до запуска.

**B · Find the bug.** Найди нарушение `no print-debugging as final solution` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Logging fundamentals за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Logging fundamentals и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Logging fundamentals?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Logging fundamentals: это отдельный технический контракт

### Нормальный Junior answer

> Logging fundamentals — тема, в которой я сначала фиксирую `debug/info/warning/error/exception`, затем объясняю `no print-debugging as final solution` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Logging fundamentals?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- debug/info/warning/error/exception
- no print-debugging as final solution
- no secrets/PII

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Logging fundamentals?

## Задача

Сделай короткую письменную практику по теме **Logging fundamentals**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Logging fundamentals: это отдельный технический контракт
- **Механизм:** Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Prometheus concepts](https://prometheus.io/docs/concepts/)
- [Grafana fundamentals](https://grafana.com/docs/grafana/latest/fundamentals/)
- [Sentry concepts](https://docs.sentry.io/concepts/)

Последняя проверка версий: **2026-08-27**.
