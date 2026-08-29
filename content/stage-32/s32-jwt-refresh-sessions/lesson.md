# JWT refresh sessions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **JWT refresh sessions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `short access token`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **JWT refresh sessions** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**short access token.** `short access token` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**server-side refresh session.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

**hashed token identifier.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

**rotation.** `rotation` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**revocation.** `revocation` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**reuse detection.** `reuse detection` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `short access token` и `server-side refresh session` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `short access token`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- short access token
- server-side refresh session
- hashed token identifier
- rotation

### Полезно

- revocation
- reuse detection

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### JWT refresh sessions: отдельный пример

```text
Сценарий: Отозвать stolen refresh.

Проверка:
Server session, rotation/revocation, short access.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `short access token` до запуска.

**B · Find the bug.** Найди нарушение `server-side refresh session` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про JWT refresh sessions за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### JWT sessions

**Сценарий:** Отозвать stolen refresh.

**Rubric:** Server session, rotation/revocation, short access.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое JWT refresh sessions и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме JWT refresh sessions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

JWT refresh sessions: это отдельный технический контракт

### Нормальный Junior answer

> JWT refresh sessions — тема, в которой я сначала фиксирую `short access token`, затем объясняю `server-side refresh session` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме JWT refresh sessions?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- short access token
- server-side refresh session
- hashed token identifier
- rotation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме JWT refresh sessions?

## Задача

Сделай короткую письменную практику по теме **JWT refresh sessions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** JWT refresh sessions: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
