# HTTP request and response

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **HTTP request and response**, а не только запомнить термин;
- прочитать и изменить короткий пример для `start line`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

HTTP — request/response protocol: request содержит method, target, headers и необязательное body, response — status, headers и необязательное body.

### Как работает

Server разбирает request, выбирает route, выполняет application logic и сериализует response. HTTP semantics отделены от JSON и framework implementation.


### Важный нюанс / ограничение

Успешная передача по сети не означает успех бизнес-операции: результат выражают status и body.

## Модель понимания

Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- start line
- method
- path
- headers

### Полезно

- body
- status

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### HTTP request and response: отдельный пример

```http
GET /examples/s12_http_request_and_response HTTP/1.1
Accept: application/json
X-Request-ID: req-12-1
```

Зафиксируй method/path/headers/body, status и поведение повторного request. Здесь route и request-id привязаны именно к теме «HTTP request and response».

## Типичные ошибки

### Ошибка 1

Ответ 200 с ошибкой внутри JSON ломает clients, monitoring и стандартную retry/cache semantics.

## Практика

**A · Предсказание результата.** Измени один input в примере `start line` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `method`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `start line`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни HTTP request and response за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое HTTP request and response и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с HTTP request and response?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

HTTP — request/response protocol: request содержит method, target, headers и необязательное body, response — status, headers и необязательное body.

### Нормальный ответ уровня Junior

> HTTP — request/response protocol: request содержит method, target, headers и необязательное body, response — status, headers и необязательное body. Server разбирает request, выбирает route, выполняет application logic и сериализует response. HTTP semantics отделены от JSON и framework implementation. Важное ограничение: Успешная передача по сети не означает успех бизнес-операции: результат выражают status и body.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с HTTP request and response?**

Ответ 200 с ошибкой внутри JSON ломает clients, monitoring и стандартную retry/cache semantics.

## Критерии хорошего ответа

### Что обязательно упомянуть

- start line
- method
- path
- headers

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Ответ 200 с ошибкой внутри JSON ломает clients, monitoring и стандартную retry/cache semantics.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с HTTP request and response?

## Задача

Сделай короткую письменную практику по теме **HTTP request and response**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** HTTP — request/response protocol: request содержит method, target, headers и необязательное body, response — status, headers и необязательное body.
- **Механизм:** Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.
- **Ограничение:** Ответ 200 с ошибкой внутри JSON ломает clients, monitoring и стандартную retry/cache semantics.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

Последняя проверка версий: **2026-08-27**.
