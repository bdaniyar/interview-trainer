# JWT pitfalls

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- объяснить `accepting wrong algorithm` своими словами и связать с backend-сценарием;
- объяснить `skipping issuer/audience/expiry` своими словами и связать с backend-сценарием;
- объяснить `storing secrets in payload` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.

В теме **JWT pitfalls** важно уверенно объяснять следующие части:

### accepting wrong algorithm

Для `accepting wrong algorithm` назови threat, trust boundary, server-side check и безопасный failure response.

### skipping issuer/audience/expiry

Для `skipping issuer/audience/expiry` назови threat, trust boundary, server-side check и безопасный failure response.

### storing secrets in payload

Для `storing secrets in payload` назови threat, trust boundary, server-side check и безопасный failure response.

### long-lived access tokens

Для `long-lived access tokens` назови threat, trust boundary, server-side check и безопасный failure response.

### unsafe browser storage

Для `unsafe browser storage` назови threat, trust boundary, server-side check и безопасный failure response.

### no revocation plan

Для `no revocation plan` назови threat, trust boundary, server-side check и безопасный failure response.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### JWT pitfalls: отдельный пример

```text
Сценарий: API декодирует payload без проверки signature/issuer/audience/exp.

Проверка:
Полная verification с разрешённым algorithm и claims; invalid token всегда безопасно отклоняется.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Считать CORS авторизацией, JWT шифрованием или хранить пароль быстрым hash.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **JWT pitfalls** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови атакующего, актив, проверку на сервере и безопасный отказ. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- accepting wrong algorithm
- skipping issuer/audience/expiry
- storing secrets in payload
- long-lived access tokens
- Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Считать CORS авторизацией, JWT шифрованием или хранить пароль быстрым hash.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- accepting wrong algorithm
- skipping issuer/audience/expiry
- storing secrets in payload
- long-lived access tokens
- unsafe browser storage
- no revocation plan.

## Задача

Разбери backend-сценарий: **Назови атакующего, актив, проверку на сервере и безопасный отказ.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Unverified JWT

**Сценарий:** API декодирует payload без проверки signature/issuer/audience/exp.

**Rubric:** Полная verification с разрешённым algorithm и claims; invalid token всегда безопасно отклоняется.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **JWT pitfalls**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
