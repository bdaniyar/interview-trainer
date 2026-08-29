# File upload design

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **File upload design**, а не только запомнить термин;
- прочитать и изменить короткий пример для `presigned URL`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **File upload design** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**presigned URL.** `presigned URL` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**object storage.** `object storage` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**metadata in PostgreSQL.** `metadata in PostgreSQL` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**validation/finalize.** `validation/finalize` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**orphan cleanup.** `orphan cleanup` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `presigned URL` и `object storage` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `presigned URL`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- presigned URL
- object storage
- metadata in PostgreSQL
- validation/finalize

### Полезно

- orphan cleanup

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### File upload design: отдельный пример

```text
Сценарий: Большой upload не через API memory.

Проверка:
Presigned URL, policy, finalize validation.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `presigned URL` до запуска.

**B · Find the bug.** Найди нарушение `object storage` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про File upload design за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### File upload

**Сценарий:** Большой upload не через API memory.

**Rubric:** Presigned URL, policy, finalize validation.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое File upload design и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме File upload design?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

File upload design: это отдельный технический контракт

### Нормальный Junior answer

> File upload design — тема, в которой я сначала фиксирую `presigned URL`, затем объясняю `object storage` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме File upload design?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- presigned URL
- object storage
- metadata in PostgreSQL
- validation/finalize

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме File upload design?

## Задача

Сделай короткую письменную практику по теме **File upload design**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** File upload design: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
