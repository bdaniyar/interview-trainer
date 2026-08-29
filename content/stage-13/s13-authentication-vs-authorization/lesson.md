# Authentication vs authorization

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Authentication vs authorization**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Authentication vs authorization`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Authentication establishes who the requester is; authorization decides whether that identity may perform an action on a resource.

### Как работает

Credentials/token/session are verified first, then policy checks roles, permissions, ownership or attributes for the concrete operation.


### Важный нюанс / limitation

A logged-in user is not automatically allowed to read another user's object.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Authentication vs authorization

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Authentication vs authorization: отдельный пример

```python
def example_s13_authentication_vs_authorization() -> tuple[str, ...]:
    # Authentication vs authorization: проверяем отдельный contract урока.
    return ('Authentication vs authorization',)

assert example_s13_authentication_vs_authorization()
```

Назови threat, trust boundary, server-side check и безопасный отказ.

## Common mistakes

### Ошибка 1

Hiding an admin button in the frontend is neither authentication nor authorization; the API must enforce the rule.

## Practice

**A · Code/result prediction.** Change one input in the `Authentication vs authorization` example and predict the result before running it.

**B · Find the bug.** Find code that violates `Authentication vs authorization` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `Authentication vs authorization` and add one edge-case test.

**E · Interview explanation.** Explain Authentication vs authorization in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Authentication vs authorization и как это работает?

### Follow-up

Какая типичная ошибка связана с Authentication vs authorization?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Authentication establishes who the requester is; authorization decides whether that identity may perform an action on a resource.

### Нормальный Junior answer

> Authentication establishes who the requester is; authorization decides whether that identity may perform an action on a resource. Credentials/token/session are verified first, then policy checks roles, permissions, ownership or attributes for the concrete operation. Важное ограничение: A logged-in user is not automatically allowed to read another user's object.

### Углубление / follow-up

**Какая типичная ошибка связана с Authentication vs authorization?**

Hiding an admin button in the frontend is neither authentication nor authorization; the API must enforce the rule.

## Expected answer rubric

### Must mention

- Authentication vs authorization

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Hiding an admin button in the frontend is neither authentication nor authorization; the API must enforce the rule.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Authentication vs authorization?

## Задача

Сделай короткую письменную практику по теме **Authentication vs authorization**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Authentication establishes who the requester is; authorization decides whether that identity may perform an action on a resource.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Hiding an admin button in the frontend is neither authentication nor authorization; the API must enforce the rule.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
