# rebase basics

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **rebase basics**, а не только запомнить термин;
- прочитать и изменить короткий пример для `replay commits`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **rebase basics** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**replay commits.** `replay commits` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**clean history.** `clean history` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**rewriting hashes.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

**do not casually rebase shared history.** Rebase переносит commits на новую base и меняет их hashes; published shared history без координации переписывать нельзя.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `replay commits` и `clean history` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `replay commits`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- replay commits
- clean history
- rewriting hashes
- do not casually rebase shared history

### Полезно

- связать rebase basics с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### rebase basics: отдельный пример

```text
Сценарий: Rebase опубликованных commits.

Проверка:
Не rebase shared; coordinate/recover refs.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `replay commits` до запуска.

**B · Find the bug.** Найди нарушение `clean history` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про rebase basics за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Shared rebase

**Сценарий:** Rebase опубликованных commits.

**Rubric:** Не rebase shared; coordinate/recover refs.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Rebase published commits

**Сценарий:** Коллеги получили divergent history после rebase main.

**Rubric:** Не переписывать shared commits; merge/revert или явно координировать rare rewrite.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое rebase basics и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме rebase basics?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

rebase basics: это отдельный технический контракт

### Нормальный Junior answer

> rebase basics — тема, в которой я сначала фиксирую `replay commits`, затем объясняю `clean history` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме rebase basics?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- replay commits
- clean history
- rewriting hashes
- do not casually rebase shared history

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме rebase basics?

## Задача

Сделай короткую письменную практику по теме **rebase basics**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** rebase basics: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
