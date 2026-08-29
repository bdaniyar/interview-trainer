# JWT structure

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **JWT structure**, а не только запомнить термин;
- прочитать и изменить короткий пример для `header`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

JWT is a signed token format with header, payload claims and signature; it is normally encoded, not encrypted.

### Как работает

The server verifies signature, allowed algorithm, issuer, audience and time claims before trusting identity/permissions.


### Важный нюанс / limitation

Revocation and refresh lifecycle still need design; a long-lived access JWT is not automatically secure or stateless in the operational sense.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- header
- payload
- signature
- encoded is not encrypted

### Полезно

- claims
- verification

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### JWT structure: отдельный пример

```python
def example_s13_jwt_structure() -> tuple[str, ...]:
    # JWT structure: проверяем отдельный contract урока.
    return ('header', 'payload', 'signature', 'encoded is not encrypted',)

assert example_s13_jwt_structure()
```

Назови threat, trust boundary, server-side check и безопасный отказ.

## Common mistakes

### Ошибка 1

Decoding payload without signature/claim verification lets an attacker supply arbitrary identity data.

## Practice

**A · Code/result prediction.** Change one input in the `header` example and predict the result before running it.

**B · Find the bug.** Find code that violates `payload` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `header` and add one edge-case test.

**E · Interview explanation.** Explain JWT structure in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое JWT structure и как это работает?

### Follow-up

Какая типичная ошибка связана с JWT structure?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

JWT is a signed token format with header, payload claims and signature; it is normally encoded, not encrypted.

### Нормальный Junior answer

> JWT is a signed token format with header, payload claims and signature; it is normally encoded, not encrypted. The server verifies signature, allowed algorithm, issuer, audience and time claims before trusting identity/permissions. Важное ограничение: Revocation and refresh lifecycle still need design; a long-lived access JWT is not automatically secure or stateless in the operational sense.

### Углубление / follow-up

**Какая типичная ошибка связана с JWT structure?**

Decoding payload without signature/claim verification lets an attacker supply arbitrary identity data.

## Expected answer rubric

### Must mention

- header
- payload
- signature
- encoded is not encrypted

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Decoding payload without signature/claim verification lets an attacker supply arbitrary identity data.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с JWT structure?

## Задача

Сделай короткую письменную практику по теме **JWT structure**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** JWT is a signed token format with header, payload claims and signature; it is normally encoded, not encrypted.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Decoding payload without signature/claim verification lets an attacker supply arbitrary identity data.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
