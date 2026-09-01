# Path, query, headers and body

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Path, query, headers and body**, а не только запомнить термин;
- прочитать и изменить короткий пример для `appropriate placement`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Как работает

Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме.

**appropriate placement.** `appropriate placement` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**validation.** `validation` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.

**sensitive data not in URL.** `sensitive data not in URL` является частью observable HTTP contract и влияет на request semantics, response status/body и допустимость повторного запроса.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `appropriate placement` и `validation` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `appropriate placement`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- appropriate placement
- validation
- sensitive data not in URL

### Полезно

- связать Path, query, headers and body с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Path, query, headers and body: отдельный пример

```http
GET /examples/s12_path_query_headers_and_body HTTP/1.1
Accept: application/json
X-Request-ID: req-12-2
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «Path, query, headers and body».

## Типичные ошибки

### Ошибка 1

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `appropriate placement` до запуска.

**B · Найди ошибку.** Найди нарушение `validation` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Path, query, headers and body за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Path, query, headers and body и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Path, query, headers and body?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Path, query, headers and body: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.

### Нормальный ответ уровня Junior

> Path, query, headers and body — тема, в которой я сначала фиксирую `appropriate placement`, затем объясняю `validation` на коротком примере. Ключевой механизм: Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме. Главная практическая ошибка — Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Path, query, headers and body?**

Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.

## Критерии хорошего ответа

### Что обязательно упомянуть

- appropriate placement
- validation
- sensitive data not in URL

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Path, query, headers and body?

## Задача

Сделай короткую письменную практику по теме **Path, query, headers and body**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Path, query, headers and body: Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
