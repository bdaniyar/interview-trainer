# JWT pitfalls

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **JWT pitfalls**, а не только запомнить термин;
- прочитать и изменить короткий пример для `accepting wrong algorithm`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Как работает

Назови asset, threat, trust boundary, server-side verification и безопасный failure result.

**accepting wrong algorithm.** `accepting wrong algorithm` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**skipping issuer/audience/expiry.** `skipping issuer/audience/expiry` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**storing secrets in payload.** `storing secrets in payload` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**long-lived access tokens.** `long-lived access tokens` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**unsafe browser storage.** `unsafe browser storage` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**no revocation plan.** `no revocation plan` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `accepting wrong algorithm` и `skipping issuer/audience/expiry` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `accepting wrong algorithm`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- accepting wrong algorithm
- skipping issuer/audience/expiry
- storing secrets in payload
- long-lived access tokens

### Полезно

- unsafe browser storage
- no revocation plan

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### JWT pitfalls: отдельный пример

```text
Сценарий: API декодирует payload без проверки signature/issuer/audience/exp.

Проверка:
Полная verification с разрешённым algorithm и claims; invalid token всегда безопасно отклоняется.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `accepting wrong algorithm` до запуска.

**B · Find the bug.** Найди нарушение `skipping issuer/audience/expiry` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про JWT pitfalls за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Unverified JWT

**Сценарий:** API декодирует payload без проверки signature/issuer/audience/exp.

**Rubric:** Полная verification с разрешённым algorithm и claims; invalid token всегда безопасно отклоняется.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое JWT pitfalls и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме JWT pitfalls?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

JWT pitfalls: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Нормальный Junior answer

> JWT pitfalls — тема, в которой я сначала фиксирую `accepting wrong algorithm`, затем объясняю `skipping issuer/audience/expiry` на коротком примере. Ключевой механизм: Назови asset, threat, trust boundary, server-side verification и безопасный failure result. Главная практическая ошибка — Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме JWT pitfalls?**

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Expected answer rubric

### Must mention

- accepting wrong algorithm
- skipping issuer/audience/expiry
- storing secrets in payload
- long-lived access tokens

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме JWT pitfalls?

## Задача

Сделай короткую письменную практику по теме **JWT pitfalls**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** JWT pitfalls: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
