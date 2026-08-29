# Why one backend language?

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why one backend language?**, а не только запомнить термин;
- прочитать и изменить короткий пример для `current scale does not justify second language`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why one backend language?** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**current scale does not justify second language.** `current scale does not justify second language` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**added build/deploy/observability complexity.** `added build/deploy/observability complexity` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**split only for measured CPU/problem/organizational boundary.** `split only for measured CPU/problem/organizational boundary` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `current scale does not justify second language` и `added build/deploy/observability complexity` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `current scale does not justify second language`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- current scale does not justify second language
- added build/deploy/observability complexity
- split only for measured CPU/problem/organizational boundary

### Полезно

- связать Why one backend language? с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why one backend language?: отдельный пример

```text
Тема: Why one backend language?

Фокус:
- current scale does not justify second language
- added build/deploy/observability complexity
- split only for measured CPU/problem/organizational boundary

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `current scale does not justify second language` до запуска.

**B · Find the bug.** Найди нарушение `added build/deploy/observability complexity` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why one backend language? за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Why one backend language? и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why one backend language??

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why one backend language?: это отдельный технический контракт

### Нормальный Junior answer

> Why one backend language? — тема, в которой я сначала фиксирую `current scale does not justify second language`, затем объясняю `added build/deploy/observability complexity` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why one backend language??**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- current scale does not justify second language
- added build/deploy/observability complexity
- split only for measured CPU/problem/organizational boundary

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why one backend language??

## Задача

Сделай короткую письменную практику по теме **Why one backend language?**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why one backend language?: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
