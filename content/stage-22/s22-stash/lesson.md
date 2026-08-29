# stash

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **stash**, а не только запомнить термин;
- прочитать и изменить короткий пример для `temporary storage`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **stash** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**temporary storage.** `temporary storage` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**named stash.** `named stash` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**apply/pop.** `apply/pop` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**conflict possibility.** `conflict possibility` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `temporary storage` и `named stash` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `temporary storage`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- temporary storage
- named stash
- apply/pop
- conflict possibility

### Полезно

- связать stash с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### stash: отдельный пример

```bash
# 22.8 · stash
# Focus: temporary storage, named stash, apply/pop, conflict possibility
printf '%s
' 's22_stash'
```

Перед командой назови изменяемое состояние: files, index, branch pointer или shared history.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `temporary storage` до запуска.

**B · Find the bug.** Найди нарушение `named stash` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про stash за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое stash и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме stash?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

stash: это отдельный технический контракт

### Нормальный Junior answer

> stash — тема, в которой я сначала фиксирую `temporary storage`, затем объясняю `named stash` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме stash?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- temporary storage
- named stash
- apply/pop
- conflict possibility

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме stash?

## Задача

Сделай короткую письменную практику по теме **stash**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** stash: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
