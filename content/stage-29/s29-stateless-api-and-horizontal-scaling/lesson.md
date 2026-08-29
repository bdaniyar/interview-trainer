# Stateless API and horizontal scaling

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Stateless API and horizontal scaling**, а не только запомнить термин;
- прочитать и изменить короткий пример для `instance-local state problem`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Stateless API and horizontal scaling** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**instance-local state problem.** `instance-local state problem` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**shared DB/cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**sticky sessions trade-off.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `instance-local state problem` и `shared DB/cache` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `instance-local state problem`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- instance-local state problem
- shared DB/cache
- sticky sessions trade-off

### Полезно

- связать Stateless API and horizontal scaling с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Stateless API and horizontal scaling: отдельный пример

```text
Сценарий: Что мешает второму API instance?

Проверка:
Local state; shared DB/cache/storage.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `instance-local state problem` до запуска.

**B · Find the bug.** Найди нарушение `shared DB/cache` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Stateless API and horizontal scaling за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Stateless API

**Сценарий:** Что мешает второму API instance?

**Rubric:** Local state; shared DB/cache/storage.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Stateless API and horizontal scaling и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Stateless API and horizontal scaling?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Stateless API and horizontal scaling: это отдельный технический контракт

### Нормальный Junior answer

> Stateless API and horizontal scaling — тема, в которой я сначала фиксирую `instance-local state problem`, затем объясняю `shared DB/cache` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Stateless API and horizontal scaling?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- instance-local state problem
- shared DB/cache
- sticky sessions trade-off

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Stateless API and horizontal scaling?

## Задача

Сделай короткую письменную практику по теме **Stateless API and horizontal scaling**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Stateless API and horizontal scaling: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
