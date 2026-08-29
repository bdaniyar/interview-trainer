# Conflict resolution

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Conflict resolution**, а не только запомнить термин;
- прочитать и изменить короткий пример для `markers`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Conflict resolution** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**markers.** `markers` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**understand both sides.** `understand both sides` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**test after resolution.** `test after resolution` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**continue/abort.** `continue/abort` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `markers` и `understand both sides` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `markers`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- markers
- understand both sides
- test after resolution
- continue/abort

### Полезно

- связать Conflict resolution с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Conflict resolution: отдельный пример

```text
Сценарий: Markers удалены, tests не запускались.

Проверка:
Понять обе стороны, stage, test.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `markers` до запуска.

**B · Find the bug.** Найди нарушение `understand both sides` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Conflict resolution за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Conflict

**Сценарий:** Markers удалены, tests не запускались.

**Rubric:** Понять обе стороны, stage, test.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Untested conflict resolution

**Сценарий:** Conflict markers удалены выбором одной стороны, контракт сломан.

**Rubric:** Понять обе версии, собрать итог вручную, inspect diff и запустить tests.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Conflict resolution и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Conflict resolution?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Conflict resolution: это отдельный технический контракт

### Нормальный Junior answer

> Conflict resolution — тема, в которой я сначала фиксирую `markers`, затем объясняю `understand both sides` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Conflict resolution?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- markers
- understand both sides
- test after resolution
- continue/abort

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Conflict resolution?

## Задача

Сделай короткую письменную практику по теме **Conflict resolution**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Conflict resolution: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
