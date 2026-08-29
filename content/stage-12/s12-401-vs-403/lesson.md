# 401 vs 403

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **401 vs 403**, а не только запомнить термин;
- прочитать и изменить короткий пример для `authentication absent/invalid`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Как работает

Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме.

**authentication absent/invalid.** Authentication устанавливает identity, authorization проверяет право этой identity выполнить конкретное действие над resource.

**authenticated but forbidden.** `authenticated but forbidden` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**appropriate challenge/header context.** `appropriate challenge/header context` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `authentication absent/invalid` и `authenticated but forbidden` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `authentication absent/invalid`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- authentication absent/invalid
- authenticated but forbidden
- appropriate challenge/header context

### Полезно

- связать 401 vs 403 с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### 401 vs 403: отдельный пример

```http
GET /examples/s12_401_vs_403 HTTP/1.1
Accept: application/json
X-Request-ID: req-12-8
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «401 vs 403».

## Common mistakes

### Ошибка 1

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `authentication absent/invalid` до запуска.

**B · Find the bug.** Найди нарушение `authenticated but forbidden` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про 401 vs 403 за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое 401 vs 403 и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме 401 vs 403?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

401 vs 403: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Нормальный Junior answer

> 401 vs 403 — тема, в которой я сначала фиксирую `authentication absent/invalid`, затем объясняю `authenticated but forbidden` на коротком примере. Ключевой механизм: Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме. Главная практическая ошибка — Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме 401 vs 403?**

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Expected answer rubric

### Must mention

- authentication absent/invalid
- authenticated but forbidden
- appropriate challenge/header context

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме 401 vs 403?

## Задача

Сделай короткую письменную практику по теме **401 vs 403**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** 401 vs 403: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
