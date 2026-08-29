# Redis-backed password reset

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Redis-backed password reset**, а не только запомнить термин;
- прочитать и изменить короткий пример для `short-lived one-time state/hashed token`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Redis-backed password reset** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**short-lived one-time state/hashed token.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

**TTL.** `TTL` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**atomic invalidation.** `atomic invalidation` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**do not reveal whether email exists.** `EXISTS` проверяет наличие хотя бы одной строки correlated subquery и часто прямо выражает semi-join без размножения строк.

**revoke sessions when appropriate.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `short-lived one-time state/hashed token` и `TTL` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `short-lived one-time state/hashed token`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- short-lived one-time state/hashed token
- TTL
- atomic invalidation
- do not reveal whether email exists

### Полезно

- revoke sessions when appropriate

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Redis-backed password reset: отдельный пример

```text
Сценарий: Один reset URL меняет пароль повторно.

Проверка:
Random high-entropy token, server-side hash, TTL и atomic one-time invalidation; revoke sessions по policy.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `short-lived one-time state/hashed token` до запуска.

**B · Find the bug.** Найди нарушение `TTL` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Redis-backed password reset за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Reusable reset token

**Сценарий:** Один reset URL меняет пароль повторно.

**Rubric:** Random high-entropy token, server-side hash, TTL и atomic one-time invalidation; revoke sessions по policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Redis-backed password reset и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Redis-backed password reset?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Redis-backed password reset: это отдельный технический контракт

### Нормальный Junior answer

> Redis-backed password reset — тема, в которой я сначала фиксирую `short-lived one-time state/hashed token`, затем объясняю `TTL` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Redis-backed password reset?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- short-lived one-time state/hashed token
- TTL
- atomic invalidation
- do not reveal whether email exists

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Redis-backed password reset?

## Задача

Сделай короткую письменную практику по теме **Redis-backed password reset**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Redis-backed password reset: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
