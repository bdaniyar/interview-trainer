# CI debugging

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **CI debugging**, а не только запомнить термин;
- прочитать и изменить короткий пример для `works locally but fails in CI`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **CI debugging** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**works locally but fails in CI.** `works locally but fails in CI` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**dependency/version/env/timezone/order differences.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**reading logs.** `reading logs` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `works locally but fails in CI` и `dependency/version/env/timezone/order differences` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `works locally but fails in CI`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- works locally but fails in CI
- dependency/version/env/timezone/order differences
- reading logs

### Полезно

- связать CI debugging с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### CI debugging: отдельный пример

```yaml
# 24.5 · CI debugging
lesson:
  key: s24_ci_debugging
  checks:
    - works locally but fails in CI
    - dependency/version/env/timezone/order differences
    - reading logs
```

CI gate должен быть воспроизводимым, иметь понятный failure log и не раскрывать secrets.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `works locally but fails in CI` до запуска.

**B · Find the bug.** Найди нарушение `dependency/version/env/timezone/order differences` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про CI debugging за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое CI debugging и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме CI debugging?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

CI debugging: это отдельный технический контракт

### Нормальный Junior answer

> CI debugging — тема, в которой я сначала фиксирую `works locally but fails in CI`, затем объясняю `dependency/version/env/timezone/order differences` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме CI debugging?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- works locally but fails in CI
- dependency/version/env/timezone/order differences
- reading logs

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме CI debugging?

## Задача

Сделай короткую письменную практику по теме **CI debugging**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** CI debugging: это отдельный технический контракт
- **Механизм:** Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub Actions documentation](https://docs.github.com/en/actions)

Последняя проверка версий: **2026-08-27**.
