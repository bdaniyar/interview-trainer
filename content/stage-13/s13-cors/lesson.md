# CORS

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **CORS**, а не только запомнить термин;
- прочитать и изменить короткий пример для `browser policy`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

CORS is a browser policy controlling whether frontend JavaScript from one origin may read responses from another origin.

### Как работает

For non-simple requests the browser sends a preflight OPTIONS request; the server returns allowed origins, methods, headers and credentials policy.


### Важный нюанс / limitation

CORS is not authentication and does not block curl or server-to-server clients.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- browser policy
- origin
- preflight
- credentials

### Полезно

- CORS is not authentication

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### CORS: отдельный пример

```text
Сценарий: Backend разрешает действие, полагаясь на blocked browser origin.

Проверка:
CORS — browser read policy; authentication/authorization проверяются на сервере для каждого request.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Using wildcard origin with credentials is invalid/unsafe; allowed origins should be explicit.

## Practice

**A · Code/result prediction.** Change one input in the `browser policy` example and predict the result before running it.

**B · Find the bug.** Find code that violates `origin` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `browser policy` and add one edge-case test.

**E · Interview explanation.** Explain CORS in 45–60 seconds and include one limitation.

## Debugging practice

### CORS as authorization

**Сценарий:** Backend разрешает действие, полагаясь на blocked browser origin.

**Rubric:** CORS — browser read policy; authentication/authorization проверяются на сервере для каждого request.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое CORS и как это работает?

### Follow-up

Какая типичная ошибка связана с CORS?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

CORS is a browser policy controlling whether frontend JavaScript from one origin may read responses from another origin.

### Нормальный Junior answer

> CORS is a browser policy controlling whether frontend JavaScript from one origin may read responses from another origin. For non-simple requests the browser sends a preflight OPTIONS request; the server returns allowed origins, methods, headers and credentials policy. Важное ограничение: CORS is not authentication and does not block curl or server-to-server clients.

### Углубление / follow-up

**Какая типичная ошибка связана с CORS?**

Using wildcard origin with credentials is invalid/unsafe; allowed origins should be explicit.

## Expected answer rubric

### Must mention

- browser policy
- origin
- preflight
- credentials

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using wildcard origin with credentials is invalid/unsafe; allowed origins should be explicit.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с CORS?

## Задача

Сделай короткую письменную практику по теме **CORS**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** CORS is a browser policy controlling whether frontend JavaScript from one origin may read responses from another origin.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Using wildcard origin with credentials is invalid/unsafe; allowed origins should be explicit.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
