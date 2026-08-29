# Basic request path

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Basic request path**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Basic request path`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Basic request path** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Basic request path.** `Basic request path` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Basic request path` и `Basic request path` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Basic request path`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Basic request path

### Полезно

- связать Basic request path с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Basic request path: отдельный пример

```text
Сценарий: Покажи путь request.

Проверка:
Boundaries, timeout, request id, source of truth.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Basic request path` до запуска.

**B · Find the bug.** Найди нарушение `Basic request path` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Basic request path за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Request path

**Сценарий:** Покажи путь request.

**Rubric:** Boundaries, timeout, request id, source of truth.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Basic request path и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Basic request path?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Basic request path: это отдельный технический контракт

### Нормальный Junior answer

> Basic request path — тема, в которой я сначала фиксирую `Basic request path`, затем объясняю `Basic request path` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Basic request path?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Basic request path

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Basic request path?

## Задача

Сделай короткую письменную практику по теме **Basic request path**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Basic request path: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
