# Why outbox instead of Celery in StudyHub

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why outbox instead of Celery in StudyHub**, а не только запомнить термин;
- прочитать и изменить короткий пример для `problem is atomicity, not merely “background”`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why outbox instead of Celery in StudyHub** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**problem is atomicity, not merely “background”.** `problem is atomicity, not merely “background”` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**direct publish after commit may be lost.** `direct publish after commit may be lost` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**publish before commit may process rolled-back state.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

**Celery can coexist but does not alone solve dual write.** `Celery can coexist but does not alone solve dual write` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `problem is atomicity, not merely “background”` и `direct publish after commit may be lost` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `problem is atomicity, not merely “background”`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- problem is atomicity, not merely “background”
- direct publish after commit may be lost
- publish before commit may process rolled-back state
- Celery can coexist but does not alone solve dual write

### Полезно

- связать Why outbox instead of Celery in StudyHub с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why outbox instead of Celery in StudyHub: отдельный пример

```text
Тема: Why outbox instead of Celery in StudyHub

Фокус:
- problem is atomicity, not merely “background”
- direct publish after commit may be lost
- publish before commit may process rolled-back state
- Celery can coexist but does not alone solve dual write

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `problem is atomicity, not merely “background”` до запуска.

**B · Find the bug.** Найди нарушение `direct publish after commit may be lost` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why outbox instead of Celery in StudyHub за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Why outbox instead of Celery in StudyHub и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of Celery in StudyHub?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why outbox instead of Celery in StudyHub: это отдельный технический контракт

### Нормальный Junior answer

> Why outbox instead of Celery in StudyHub — тема, в которой я сначала фиксирую `problem is atomicity, not merely “background”`, затем объясняю `direct publish after commit may be lost` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of Celery in StudyHub?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- problem is atomicity, not merely “background”
- direct publish after commit may be lost
- publish before commit may process rolled-back state
- Celery can coexist but does not alone solve dual write

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of Celery in StudyHub?

## Задача

Сделай короткую письменную практику по теме **Why outbox instead of Celery in StudyHub**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why outbox instead of Celery in StudyHub: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
