# Hotel Booking and double booking

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Hotel Booking and double booking**, а не только запомнить термин;
- прочитать и изменить короткий пример для `separate SELECT is insufficient`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Hotel Booking and double booking** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**separate SELECT is insufficient.** `SELECT` формирует result columns после FROM/JOIN/WHERE/GROUP/HAVING; порядок строк существует только при явном `ORDER BY`.

**DB constraint/conditional write/lock.** Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

**short transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**`409 Conflict`.** ``409 Conflict`` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**idempotency where applicable.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `separate SELECT is insufficient` и `DB constraint/conditional write/lock` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `separate SELECT is insufficient`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- separate SELECT is insufficient
- DB constraint/conditional write/lock
- short transaction
- `409 Conflict`

### Полезно

- idempotency where applicable

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Hotel Booking and double booking: отдельный пример

```text
Сценарий: Не допустить double booking.

Проверка:
DB invariant, short transaction, concurrent test.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `separate SELECT is insufficient` до запуска.

**B · Find the bug.** Найди нарушение `DB constraint/conditional write/lock` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Hotel Booking and double booking за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Hotel race

**Сценарий:** Не допустить double booking.

**Rubric:** DB invariant, short transaction, concurrent test.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Hotel Booking and double booking и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Hotel Booking and double booking?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Hotel Booking and double booking: это отдельный технический контракт

### Нормальный Junior answer

> Hotel Booking and double booking — тема, в которой я сначала фиксирую `separate SELECT is insufficient`, затем объясняю `DB constraint/conditional write/lock` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Hotel Booking and double booking?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- separate SELECT is insufficient
- DB constraint/conditional write/lock
- short transaction
- `409 Conflict`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Hotel Booking and double booking?

## Задача

Сделай короткую письменную практику по теме **Hotel Booking and double booking**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Hotel Booking and double booking: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
