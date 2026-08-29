# CSRF

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **CSRF**, а не только запомнить термин;
- прочитать и изменить короткий пример для `browser automatically sends cookies`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Как работает

Назови asset, threat, trust boundary, server-side verification и безопасный failure result.

**browser automatically sends cookies.** `browser automatically sends cookies` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**SameSite.** `SameSite` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**CSRF token.** CSRF использует автоматически отправляемые browser credentials; защита включает SameSite и CSRF token/origin checks для state-changing requests.

**bearer header differences.** `bearer header differences` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `browser automatically sends cookies` и `SameSite` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `browser automatically sends cookies`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- browser automatically sends cookies
- SameSite
- CSRF token
- bearer header differences

### Полезно

- связать CSRF с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### CSRF: отдельный пример

```python
def example_s13_csrf() -> tuple[str, ...]:
    # CSRF: проверяем отдельный contract урока.
    return ('browser automatically sends cookies', 'SameSite', 'CSRF token', 'bearer header differences',)

assert example_s13_csrf()
```

Назови threat, trust boundary, server-side check и безопасный отказ.

## Common mistakes

### Ошибка 1

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `browser automatically sends cookies` до запуска.

**B · Find the bug.** Найди нарушение `SameSite` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про CSRF за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое CSRF и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме CSRF?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

CSRF: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Нормальный Junior answer

> CSRF — тема, в которой я сначала фиксирую `browser automatically sends cookies`, затем объясняю `SameSite` на коротком примере. Ключевой механизм: Назови asset, threat, trust boundary, server-side verification и безопасный failure result. Главная практическая ошибка — Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме CSRF?**

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Expected answer rubric

### Must mention

- browser automatically sends cookies
- SameSite
- CSRF token
- bearer header differences

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме CSRF?

## Задача

Сделай короткую письменную практику по теме **CSRF**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** CSRF: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
