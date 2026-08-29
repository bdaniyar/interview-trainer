# GitHub Actions or existing CI

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **GitHub Actions or existing CI**, а не только запомнить термин;
- прочитать и изменить короткий пример для `workflow`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **GitHub Actions or existing CI** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**workflow.** `workflow` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**trigger.** `trigger` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**job.** `job` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**step.** `step` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**secrets.** `secrets` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `workflow` и `trigger` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `workflow`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- workflow
- trigger
- job
- step

### Полезно

- cache
- secrets

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### GitHub Actions or existing CI: отдельный пример

```yaml
# 24.3 · GitHub Actions or existing CI
lesson:
  key: s24_github_actions_or_existing_ci
  checks:
    - workflow
    - trigger
    - job
    - step
```

CI gate должен быть воспроизводимым, иметь понятный failure log и не раскрывать secrets.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `workflow` до запуска.

**B · Find the bug.** Найди нарушение `trigger` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про GitHub Actions or existing CI за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое GitHub Actions or existing CI и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме GitHub Actions or existing CI?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

GitHub Actions or existing CI: это отдельный технический контракт

### Нормальный Junior answer

> GitHub Actions or existing CI — тема, в которой я сначала фиксирую `workflow`, затем объясняю `trigger` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме GitHub Actions or existing CI?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- workflow
- trigger
- job
- step

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме GitHub Actions or existing CI?

## Задача

Сделай короткую письменную практику по теме **GitHub Actions or existing CI**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** GitHub Actions or existing CI: это отдельный технический контракт
- **Механизм:** Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub Actions documentation](https://docs.github.com/en/actions)

Последняя проверка версий: **2026-08-27**.
