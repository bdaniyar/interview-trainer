# SQL injection

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- объяснить `parameterized queries` своими словами и связать с backend-сценарием;
- объяснить `ORM does not protect raw string interpolation` своими словами и связать с backend-сценарием;
- объяснить `identifiers/order fields require allowlist.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.

В теме **SQL injection** важно уверенно объяснять следующие части:

### parameterized queries

Для `parameterized queries` назови threat, trust boundary, server-side check и безопасный failure response.

### ORM does not protect raw string interpolation

Для `ORM does not protect raw string interpolation` назови threat, trust boundary, server-side check и безопасный failure response.

### identifiers/order fields require allowlist

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

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

1. Объясни **SQL injection** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови атакующего, актив, проверку на сервере и безопасный отказ. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- parameterized queries
- ORM does not protect raw string interpolation
- identifiers/order fields require allowlist.
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

- parameterized queries
- ORM does not protect raw string interpolation
- identifiers/order fields require allowlist.

## Задача

Разбери backend-сценарий: **Назови атакующего, актив, проверку на сервере и безопасный отказ.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### SQL f-string

**Сценарий:** Query строится из user input через f-string.

**Rubric:** Parameterized query/SQLAlchemy expression; test malicious input как data, не SQL syntax.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **SQL injection**;
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
