# Layers and cache

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Layers and cache**, а не только запомнить термин;
- прочитать и изменить короткий пример для `dependency files first`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Layers and cache** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**dependency files first.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**source later.** `source later` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**cache invalidation.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `dependency files first` и `source later` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `dependency files first`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- dependency files first
- source later
- cache invalidation

### Полезно

- связать Layers and cache с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Layers and cache: отдельный пример

```yaml
# 21.3 · Layers and cache
lesson:
  key: s21_layers_and_cache
  checks:
    - dependency files first
    - source later
    - cache invalidation
```

Разделяй build-time image и runtime container: DNS, ports, mounts, env и readiness.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `dependency files first` до запуска.

**B · Find the bug.** Найди нарушение `source later` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Layers and cache за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Layers and cache и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Layers and cache?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Layers and cache: это отдельный технический контракт

### Нормальный Junior answer

> Layers and cache — тема, в которой я сначала фиксирую `dependency files first`, затем объясняю `source later` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Layers and cache?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- dependency files first
- source later
- cache invalidation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Layers and cache?

## Задача

Сделай короткую письменную практику по теме **Layers and cache**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Layers and cache: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
