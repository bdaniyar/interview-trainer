# Access and refresh tokens

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- объяснить `short-lived access` своими словами и связать с backend-сценарием;
- объяснить `longer refresh` своими словами и связать с backend-сценарием;
- объяснить `rotation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.

В теме **Access and refresh tokens** важно уверенно объяснять следующие части:

### short-lived access

Для `short-lived access` назови threat, trust boundary, server-side check и безопасный failure response.

### longer refresh

Для `longer refresh` назови threat, trust boundary, server-side check и безопасный failure response.

### rotation

Для `rotation` назови threat, trust boundary, server-side check и безопасный failure response.

### revocation

Для `revocation` назови threat, trust boundary, server-side check и безопасный failure response.

### reuse detection

Для `reuse detection` назови threat, trust boundary, server-side check и безопасный failure response.

### server-side refresh session

Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
def can_edit(user, article) -> bool:
    return user.id == article.author_id or "moderator" in user.roles
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Считать CORS авторизацией, JWT шифрованием или хранить пароль быстрым hash.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Access and refresh tokens** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови атакующего, актив, проверку на сервере и безопасный отказ. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- short-lived access
- longer refresh
- rotation
- revocation
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

- short-lived access
- longer refresh
- rotation
- revocation
- reuse detection
- server-side refresh session.

## Задача

Разбери backend-сценарий: **Назови атакующего, актив, проверку на сервере и безопасный отказ.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Long-lived access token

**Сценарий:** Украденный access действует месяц без возможности быстро ограничить ущерб.

**Rubric:** Короткий access, controlled refresh session/rotation/revocation; threat-based TTL.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Access and refresh tokens**;
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
