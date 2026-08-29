# MinIO and presigned URLs

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **MinIO and presigned URLs**, а не только запомнить термин;
- прочитать и изменить короткий пример для `S3-compatible object storage`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **MinIO and presigned URLs** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**S3-compatible object storage.** `S3-compatible object storage` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**short-lived direct upload.** `short-lived direct upload` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**metadata/key in PostgreSQL.** `metadata/key in PostgreSQL` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**authorization.** Authorization выполняется server-side на каждом resource/action и не заменяется скрытой кнопкой, CORS или данными из непроверенного token.

**finalize validation.** `finalize validation` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**no raw binary in relational row.** `no raw binary in relational row` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `S3-compatible object storage` и `short-lived direct upload` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `S3-compatible object storage`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- S3-compatible object storage
- short-lived direct upload
- metadata/key in PostgreSQL
- authorization

### Полезно

- finalize validation
- no raw binary in relational row

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### MinIO and presigned URLs: отдельный пример

```text
Сценарий: Слишком большой file.

Проверка:
Policy, size validation, delete/reject.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `S3-compatible object storage` до запуска.

**B · Find the bug.** Найди нарушение `short-lived direct upload` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про MinIO and presigned URLs за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Presigned upload

**Сценарий:** Слишком большой file.

**Rubric:** Policy, size validation, delete/reject.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое MinIO and presigned URLs и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме MinIO and presigned URLs?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

MinIO and presigned URLs: это отдельный технический контракт

### Нормальный Junior answer

> MinIO and presigned URLs — тема, в которой я сначала фиксирую `S3-compatible object storage`, затем объясняю `short-lived direct upload` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме MinIO and presigned URLs?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- S3-compatible object storage
- short-lived direct upload
- metadata/key in PostgreSQL
- authorization

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме MinIO and presigned URLs?

## Задача

Сделай короткую письменную практику по теме **MinIO and presigned URLs**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** MinIO and presigned URLs: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
