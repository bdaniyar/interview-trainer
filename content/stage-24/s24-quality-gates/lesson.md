# Quality gates

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Quality gates**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Ruff`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Quality gates** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Ruff.** `Ruff` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**tests.** `tests` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**typecheck.** `typecheck` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**coverage.** Coverage показывает исполненные строки/ветки, но не доказывает качество assertions и полноту failure scenarios.

**build.** `build` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.

**gates do not guarantee correctness.** `gates do not guarantee correctness` является частью reproducible CI/CD gate с явным trigger, versioned artifact и безопасной передачей secrets.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Ruff` и `tests` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Ruff`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Ruff
- tests
- typecheck
- coverage

### Полезно

- build
- gates do not guarantee correctness

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Quality gates: отдельный пример

```yaml
# 24.4 · Quality gates
lesson:
  key: s24_quality_gates
  checks:
    - Ruff
    - tests
    - typecheck
    - coverage
```

CI gate должен быть воспроизводимым, иметь понятный failure log и не раскрывать secrets.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Ruff` до запуска.

**B · Find the bug.** Найди нарушение `tests` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Quality gates за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Quality gates и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Quality gates?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Quality gates: это отдельный технический контракт

### Нормальный Junior answer

> Quality gates — тема, в которой я сначала фиксирую `Ruff`, затем объясняю `tests` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Quality gates?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Ruff
- tests
- typecheck
- coverage

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Quality gates?

## Задача

Сделай короткую письменную практику по теме **Quality gates**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Quality gates: это отдельный технический контракт
- **Механизм:** Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub Actions documentation](https://docs.github.com/en/actions)

Последняя проверка версий: **2026-08-27**.
