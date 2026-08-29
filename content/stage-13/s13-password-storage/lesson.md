# Password storage

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Password storage**, а не только запомнить термин;
- прочитать и изменить короткий пример для `password hashing`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Как работает

Назови asset, threat, trust boundary, server-side verification и безопасный failure result.

**password hashing.** Пароль хранят через специализированный медленный password hash с солью, а не через быстрый общий hash.

**salt.** `salt` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**work factor.** `work factor` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**Argon2/bcrypt concepts.** `Argon2/bcrypt concepts` закрывает конкретную threat на trust boundary; проверка выполняется server-side, а отказ не раскрывает лишних данных.

**never reversible encryption/plain hash.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `password hashing` и `salt` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `password hashing`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- password hashing
- salt
- work factor
- Argon2/bcrypt concepts

### Полезно

- never reversible encryption/plain hash

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Password storage: отдельный пример

```text
Сценарий: Пароли сохранены через один SHA-256.

Проверка:
Argon2id/bcrypt/scrypt с индивидуальной солью и cost; тест verify и migration policy.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `password hashing` до запуска.

**B · Find the bug.** Найди нарушение `salt` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Password storage за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Fast password hash

**Сценарий:** Пароли сохранены через один SHA-256.

**Rubric:** Argon2id/bcrypt/scrypt с индивидуальной солью и cost; тест verify и migration policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Password storage и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Password storage?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Password storage: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.

### Нормальный Junior answer

> Password storage — тема, в которой я сначала фиксирую `password hashing`, затем объясняю `salt` на коротком примере. Ключевой механизм: Назови asset, threat, trust boundary, server-side verification и безопасный failure result. Главная практическая ошибка — Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Password storage?**

Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.

## Expected answer rubric

### Must mention

- password hashing
- salt
- work factor
- Argon2/bcrypt concepts

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Password storage?

## Задача

Сделай короткую письменную практику по теме **Password storage**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Password storage: Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.
- **Механизм:** Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.
- **Ограничение:** Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)

Последняя проверка версий: **2026-08-27**.
