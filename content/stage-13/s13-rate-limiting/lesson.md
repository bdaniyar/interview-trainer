# Rate limiting

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- объяснить `abuse control` своими словами и связать с backend-сценарием;
- объяснить `per-user/IP/action` своими словами и связать с backend-сценарием;
- объяснить `fixed/sliding/token bucket concepts` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.

В теме **Rate limiting** важно уверенно объяснять следующие части:

### abuse control

Для `abuse control` назови threat, trust boundary, server-side check и безопасный failure response.

### per-user/IP/action

Для `per-user/IP/action` назови threat, trust boundary, server-side check и безопасный failure response.

### fixed/sliding/token bucket concepts

Для `fixed/sliding/token bucket concepts` назови threat, trust boundary, server-side check и безопасный failure response.

### Redis atomic counters

Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.

### 429

Для `429` назови threat, trust boundary, server-side check и безопасный failure response.

### fail-open/fail-closed trade-off

Для `fail-open/fail-closed trade-off` назови threat, trust boundary, server-side check и безопасный failure response.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Rate limiting: отдельный пример

```python
def example_s13_rate_limiting() -> tuple[str, ...]:
    # Rate limiting: проверяем отдельный contract урока.
    return ('abuse control', 'per-user/IP/action', 'fixed/sliding/token bucket concepts', 'Redis atomic counters',)

assert example_s13_rate_limiting()
```

Назови threat, trust boundary, server-side check и безопасный отказ.

## Common mistakes

**Ошибка:** Считать CORS авторизацией, JWT шифрованием или хранить пароль быстрым hash.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Rate limiting** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Назови атакующего, актив, проверку на сервере и безопасный отказ. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- abuse control
- per-user/IP/action
- fixed/sliding/token bucket concepts
- Redis atomic counters
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

- abuse control
- per-user/IP/action
- fixed/sliding/token bucket concepts
- Redis atomic counters
- 429
- fail-open/fail-closed trade-off.

## Задача

Разбери backend-сценарий: **Назови атакующего, актив, проверку на сервере и безопасный отказ.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Rate limiting**;
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
