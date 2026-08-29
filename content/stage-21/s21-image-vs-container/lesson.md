# Image vs container

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Image vs container**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Image vs container`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Image vs container** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Image vs container.** Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Image vs container` и `Image vs container` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Image vs container`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Image vs container

### Полезно

- связать Image vs container с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Image vs container: отдельный пример

```yaml
# 21.1 · Image vs container
lesson:
  key: s21_image_vs_container
  checks:
    - Image vs container
```

Разделяй build-time image и runtime container: DNS, ports, mounts, env и readiness.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Image vs container` до запуска.

**B · Find the bug.** Найди нарушение `Image vs container` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Image vs container за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Image vs container и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Image vs container?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Image vs container: это отдельный технический контракт

### Нормальный Junior answer

> Image vs container — тема, в которой я сначала фиксирую `Image vs container`, затем объясняю `Image vs container` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Image vs container?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Image vs container

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Image vs container?

## Задача

Сделай короткую письменную практику по теме **Image vs container**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Image vs container: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
