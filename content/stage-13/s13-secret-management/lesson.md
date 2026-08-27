# Secret management

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- объяснить `environment/config` своими словами и связать с backend-сценарием;
- объяснить `no secrets in image/repo` своими словами и связать с backend-сценарием;
- объяснить `rotation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.

В теме **Secret management** важно уверенно объяснять следующие части:

### environment/config

Для `environment/config` назови threat, trust boundary, server-side check и безопасный failure response.

### no secrets in image/repo

Для `no secrets in image/repo` назови threat, trust boundary, server-side check и безопасный failure response.

### rotation

Для `rotation` назови threat, trust boundary, server-side check и безопасный failure response.

### `.env.example`

Для ``.env.example`` назови threat, trust boundary, server-side check и безопасный failure response.

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

1. Объясни **Secret management** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови атакующего, актив, проверку на сервере и безопасный отказ. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- environment/config
- no secrets in image/repo
- rotation
- `.env.example`.
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

- environment/config
- no secrets in image/repo
- rotation
- `.env.example`.

## Задача

Разбери backend-сценарий: **Назови атакующего, актив, проверку на сервере и безопасный отказ.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Secret management**;
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
