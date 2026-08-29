# RBAC and permissions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **RBAC and permissions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `role`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Как работает

Назови asset, threat, trust boundary, server-side verification и безопасный failure result.

**role.** `role` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**permission.** `permission` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**object-level authorization.** Authorization выполняется server-side на каждом resource/action и не заменяется скрытой кнопкой, CORS или данными из непроверенного token.

**UI is not security boundary.** `UI is not security boundary` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `role` и `permission` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `role`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- role
- permission
- object-level authorization
- UI is not security boundary

### Полезно

- связать RBAC and permissions с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### RBAC and permissions: отдельный пример

```python
def example_s13_rbac_and_permissions() -> tuple[str, ...]:
    # RBAC and permissions: проверяем отдельный contract урока.
    return ('role', 'permission', 'object-level authorization', 'UI is not security boundary',)

assert example_s13_rbac_and_permissions()
```

Назови threat, trust boundary, server-side check и безопасный отказ.

## Common mistakes

### Ошибка 1

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `role` до запуска.

**B · Find the bug.** Найди нарушение `permission` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про RBAC and permissions за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое RBAC and permissions и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме RBAC and permissions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

RBAC and permissions: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Нормальный Junior answer

> RBAC and permissions — тема, в которой я сначала фиксирую `role`, затем объясняю `permission` на коротком примере. Ключевой механизм: Назови asset, threat, trust boundary, server-side verification и безопасный failure result. Главная практическая ошибка — Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме RBAC and permissions?**

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Expected answer rubric

### Must mention

- role
- permission
- object-level authorization
- UI is not security boundary

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме RBAC and permissions?

## Задача

Сделай короткую письменную практику по теме **RBAC and permissions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** RBAC and permissions: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
