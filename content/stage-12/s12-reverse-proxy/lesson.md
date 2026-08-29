# Reverse proxy

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Reverse proxy**, а не только запомнить термин;
- прочитать и изменить короткий пример для `client → Nginx/proxy → application`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Как работает

Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме.

**client → Nginx/proxy → application.** `client → Nginx/proxy → application` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**TLS termination.** `TLS termination` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**headers.** `headers` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**load distribution.** `load distribution` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `client → Nginx/proxy → application` и `TLS termination` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `client → Nginx/proxy → application`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- client → Nginx/proxy → application
- TLS termination
- headers
- load distribution

### Полезно

- связать Reverse proxy с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Reverse proxy: отдельный пример

```http
GET /examples/s12_reverse_proxy HTTP/1.1
Accept: application/json
X-Request-ID: req-12-17
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Reverse proxy».

## Common mistakes

### Ошибка 1

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `client → Nginx/proxy → application` до запуска.

**B · Find the bug.** Найди нарушение `TLS termination` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Reverse proxy за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Reverse proxy и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Reverse proxy?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Reverse proxy: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Нормальный Junior answer

> Reverse proxy — тема, в которой я сначала фиксирую `client → Nginx/proxy → application`, затем объясняю `TLS termination` на коротком примере. Ключевой механизм: Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме. Главная практическая ошибка — Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Reverse proxy?**

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Expected answer rubric

### Must mention

- client → Nginx/proxy → application
- TLS termination
- headers
- load distribution

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Reverse proxy?

## Задача

Сделай короткую письменную практику по теме **Reverse proxy**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Reverse proxy: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
