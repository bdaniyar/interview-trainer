# CI debugging

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.

## Learning objectives

После урока ты сможешь:

- объяснить `works locally but fails in CI` своими словами и связать с backend-сценарием;
- объяснить `dependency/version/env/timezone/order differences` своими словами и связать с backend-сценарием;
- объяснить `reading logs.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

CI повторяемо выполняет quality gates для commit; CD продвигает проверенный artifact по окружениям.

В теме **CI debugging** важно уверенно объяснять следующие части:

### works locally but fails in CI

Для `works locally but fails in CI` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

### dependency/version/env/timezone/order differences

Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

### reading logs

Для `reading logs` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

## Mental model

Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Игнорировать flaky test или собирать другой код на каждом environment.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **CI debugging** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери failure по шагу, версии runtime, env и отличию от local run. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- works locally but fails in CI
- dependency/version/env/timezone/order differences
- reading logs.
- Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Игнорировать flaky test или собирать другой код на каждом environment.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- works locally but fails in CI
- dependency/version/env/timezone/order differences
- reading logs.

## Задача

Разбери backend-сценарий: **Разбери failure по шагу, версии runtime, env и отличию от local run.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **CI debugging**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub Actions documentation](https://docs.github.com/en/actions)

Последняя проверка версий: **2026-08-27**.
