# reset vs revert

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **reset vs revert**, а не только запомнить термин;
- прочитать и изменить короткий пример для `local history movement`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **reset vs revert** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**local history movement.** `local history movement` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.

**working/index effects.** Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

**safe public-history undo.** `safe public-history undo` меняет одно из состояний Git: working tree, index, branch pointer или shared history; эти эффекты нельзя смешивать.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `local history movement` и `working/index effects` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `local history movement`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- local history movement
- working/index effects
- safe public-history undo

### Полезно

- связать reset vs revert с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### reset vs revert: отдельный пример

```text
Сценарий: Ошибка уже в main.

Проверка:
git revert; не rewrite shared history.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `local history movement` до запуска.

**B · Find the bug.** Найди нарушение `working/index effects` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про reset vs revert за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Undo public commit

**Сценарий:** Ошибка уже в main.

**Rubric:** git revert; не rewrite shared history.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Reset shared branch

**Сценарий:** force push после reset удалил commits коллег.

**Rubric:** Для published history использовать revert; recovery через reflog/remote refs и coordination.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое reset vs revert и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме reset vs revert?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

reset vs revert: это отдельный технический контракт

### Нормальный Junior answer

> reset vs revert — тема, в которой я сначала фиксирую `local history movement`, затем объясняю `working/index effects` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме reset vs revert?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- local history movement
- working/index effects
- safe public-history undo

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме reset vs revert?

## Задача

Сделай короткую письменную практику по теме **reset vs revert**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** reset vs revert: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
