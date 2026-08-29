# Practical Git scenarios

> [!IMPORTANT]
> **P0 · вероятность на интервью: medium · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Practical Git scenarios**, а не только запомнить термин;
- прочитать и изменить короткий пример для `wrong branch`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Practical Git scenarios** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**wrong branch.** `wrong branch` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**accidental commit.** `accidental commit` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**merge conflict.** `merge conflict` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**undo public change.** `undo public change` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**recover stashed work.** `recover stashed work` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**sync with main.** `sync with main` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `wrong branch` и `accidental commit` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `wrong branch`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- wrong branch
- accidental commit
- merge conflict
- undo public change

### Полезно

- recover stashed work
- sync with main

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Practical Git scenarios: отдельный пример

```text
Сценарий: Commit случайно в main local.

Проверка:
Создать branch at commit; безопасно restore main.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `wrong branch` до запуска.

**B · Find the bug.** Найди нарушение `accidental commit` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Practical Git scenarios за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Wrong branch

**Сценарий:** Commit случайно в main local.

**Rubric:** Создать branch at commit; безопасно restore main.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Practical Git scenarios и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Practical Git scenarios?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Practical Git scenarios: это отдельный технический контракт

### Нормальный Junior answer

> Practical Git scenarios — тема, в которой я сначала фиксирую `wrong branch`, затем объясняю `accidental commit` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Practical Git scenarios?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- wrong branch
- accidental commit
- merge conflict
- undo public change

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Practical Git scenarios?

## Задача

Сделай короткую письменную практику по теме **Practical Git scenarios**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Practical Git scenarios: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
