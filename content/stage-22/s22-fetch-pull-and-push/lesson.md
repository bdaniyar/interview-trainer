# fetch, pull and push

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **fetch, pull and push**, а не только запомнить термин;
- прочитать и изменить короткий пример для `pull as fetch + integration`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **fetch, pull and push** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**pull as fetch + integration.** `pull as fetch + integration` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**upstream branch.** `upstream branch` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `pull as fetch + integration` и `upstream branch` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `pull as fetch + integration`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- pull as fetch + integration
- upstream branch

### Полезно

- связать fetch, pull and push с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### fetch, pull and push: отдельный пример

```bash
# 22.4 · fetch, pull and push
# Focus: pull as fetch + integration, upstream branch
printf '%s
' 's22_fetch_pull_and_push'
```

Перед командой назови изменяемое состояние: files, index, branch pointer или shared history.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `pull as fetch + integration` до запуска.

**B · Find the bug.** Найди нарушение `upstream branch` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про fetch, pull and push за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое fetch, pull and push и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме fetch, pull and push?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

fetch, pull and push: это отдельный технический контракт

### Нормальный Junior answer

> fetch, pull and push — тема, в которой я сначала фиксирую `pull as fetch + integration`, затем объясняю `upstream branch` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме fetch, pull and push?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- pull as fetch + integration
- upstream branch

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме fetch, pull and push?

## Задача

Сделай короткую письменную практику по теме **fetch, pull and push**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** fetch, pull and push: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
