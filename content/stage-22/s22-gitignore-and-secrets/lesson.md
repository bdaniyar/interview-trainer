# `.gitignore` and secrets

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`.gitignore` and secrets**, а не только запомнить термин;
- прочитать и изменить короткий пример для `ignoring future files does not remove tracked/history content`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **`.gitignore` and secrets** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**ignoring future files does not remove tracked/history content.** `ignoring future files does not remove tracked/history content` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**leaked secret must be rotated.** `leaked secret must be rotated` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `ignoring future files does not remove tracked/history content` и `leaked secret must be rotated` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `ignoring future files does not remove tracked/history content`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- ignoring future files does not remove tracked/history content
- leaked secret must be rotated

### Полезно

- связать `.gitignore` and secrets с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `.gitignore` and secrets: отдельный пример

```text
Сценарий: Secret удалён из file.

Проверка:
Rotate; audit; history cleanup отдельно.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `ignoring future files does not remove tracked/history content` до запуска.

**B · Find the bug.** Найди нарушение `leaked secret must be rotated` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `.gitignore` and secrets за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Leaked token

**Сценарий:** Secret удалён из file.

**Rubric:** Rotate; audit; history cleanup отдельно.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Secret still active

**Сценарий:** Token удалён из Git, но им продолжают пользоваться.

**Rubric:** Немедленно revoke/rotate, затем audit и при необходимости clean history; gitignore не лечит leak.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `.gitignore` and secrets и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `.gitignore` and secrets?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`.gitignore` and secrets: это отдельный технический контракт

### Нормальный Junior answer

> `.gitignore` and secrets — тема, в которой я сначала фиксирую `ignoring future files does not remove tracked/history content`, затем объясняю `leaked secret must be rotated` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `.gitignore` and secrets?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- ignoring future files does not remove tracked/history content
- leaked secret must be rotated

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `.gitignore` and secrets?

## Задача

Сделай короткую письменную практику по теме **`.gitignore` and secrets**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `.gitignore` and secrets: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
