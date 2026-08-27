# Quality gates

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.

## Learning objectives

После урока ты сможешь:

- объяснить `Ruff` своими словами и связать с backend-сценарием;
- объяснить `tests` своими словами и связать с backend-сценарием;
- объяснить `typecheck` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

CI повторяемо выполняет quality gates для commit; CD продвигает проверенный artifact по окружениям.

В теме **Quality gates** важно уверенно объяснять следующие части:

### Ruff

Для `Ruff` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

### tests

Для `tests` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

### typecheck

Для `typecheck` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

### coverage

Coverage показывает исполненные строки/ветки, но не доказывает качество assertions и полноту failure scenarios.

### build

Для `build` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

### gates do not guarantee correctness

Для `gates do not guarantee correctness` определи reproducible quality gate, trigger, artifact и безопасное управление secret.

## Mental model

Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```yaml
steps:
  - run: python -m pytest
  - run: ruff check .
  - run: docker build -t app:${GITHUB_SHA} .
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Игнорировать flaky test или собирать другой код на каждом environment.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Quality gates** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Разбери failure по шагу, версии runtime, env и отличию от local run. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- Ruff
- tests
- typecheck
- coverage
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

- Ruff
- tests
- typecheck
- coverage
- build
- gates do not guarantee correctness.

## Задача

Разбери backend-сценарий: **Разбери failure по шагу, версии runtime, env и отличию от local run.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Quality gates**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub Actions documentation](https://docs.github.com/en/actions)

Последняя проверка версий: **2026-08-27**.
