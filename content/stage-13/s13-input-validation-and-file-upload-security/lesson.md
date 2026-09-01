# Input validation and file upload security

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Input validation and file upload security**, а не только запомнить термин;
- прочитать и изменить короткий пример для `size`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Как работает

Назови asset, threat, trust boundary, на стороне сервера verification и безопасный failure result.

**size.** `size` закрывает конкретную threat на trust boundary; проверка выполняется на стороне сервера, а отказ не раскрывает лишних данных.

**type.** `type` закрывает конкретную threat на trust boundary; проверка выполняется на стороне сервера, а отказ не раскрывает лишних данных.

**filename/key.** `filename/key` закрывает конкретную threat на trust boundary; проверка выполняется на стороне сервера, а отказ не раскрывает лишних данных.

**content inspection limitations.** `content inspection limitations` закрывает конкретную threat на trust boundary; проверка выполняется на стороне сервера, а отказ не раскрывает лишних данных.

**authorization.** Authorization выполняется на стороне сервера на каждом resource/action и не заменяется скрытой кнопкой, CORS или данными из непроверенного token.

**orphan cleanup.** `orphan cleanup` закрывает конкретную threat на trust boundary; проверка выполняется на стороне сервера, а отказ не раскрывает лишних данных.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `size` и `type` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `size`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- size
- type
- filename/key
- content inspection limitations

### Полезно

- authorization
- orphan cleanup

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Input validation and file upload security: отдельный пример

```python
def example_s13_input_validation_and_file_upload_security() -> tuple[str, ...]:
    # Input validation and file upload security: проверяем отдельный contract урока.
    return ('size', 'type', 'filename/key', 'content inspection limitations',)

assert example_s13_input_validation_and_file_upload_security()
```

Назови threat, trust boundary, на стороне сервера check и безопасный отказ.

## Типичные ошибки

### Ошибка 1

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `size` до запуска.

**B · Найди ошибку.** Найди нарушение `type` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Input validation and file upload security за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Input validation and file upload security и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Input validation and file upload security?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Input validation and file upload security: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Нормальный ответ уровня Junior

> Input validation and file upload security — тема, в которой я сначала фиксирую `size`, затем объясняю `type` на коротком примере. Ключевой механизм: Назови asset, threat, trust boundary, на стороне сервера verification и безопасный failure result. Главная практическая ошибка — Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Input validation and file upload security?**

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Критерии хорошего ответа

### Что обязательно упомянуть

- size
- type
- filename/key
- content inspection limitations

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Input validation and file upload security?

## Задача

Сделай короткую письменную практику по теме **Input validation and file upload security**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Input validation and file upload security: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
