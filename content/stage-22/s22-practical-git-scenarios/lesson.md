# Practical Git scenarios

> [!IMPORTANT]
> **P0 · вероятность на интервью: medium · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `wrong branch` своими словами и связать с backend-сценарием;
- объяснить `accidental commit` своими словами и связать с backend-сценарием;
- объяснить `merge conflict` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Git хранит snapshots и граф commits; working tree, index, local branch и remote-tracking branch — разные состояния.

В теме **Practical Git scenarios** важно уверенно объяснять следующие части:

### wrong branch

Для `wrong branch` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### accidental commit

Для `accidental commit` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### merge conflict

Для `merge conflict` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### undo public change

Для `undo public change` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### recover stashed work

Для `recover stashed work` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### sync with main

Для `sync with main` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```bash
git status
git add backend/app.py tests/test_app.py
git commit -m "fix booking conflict handling"
git push -u origin fix/booking-conflict
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Rebase shared commits или удалять secret из файла без ротации.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Practical Git scenarios** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери безопасный способ отменить локальное и уже опубликованное изменение. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- wrong branch
- accidental commit
- merge conflict
- undo public change
- Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Rebase shared commits или удалять secret из файла без ротации.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- wrong branch
- accidental commit
- merge conflict
- undo public change
- recover stashed work
- sync with main.

## Задача

Разбери backend-сценарий: **Выбери безопасный способ отменить локальное и уже опубликованное изменение.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Operations practice

### Wrong branch

**Сценарий:** Commit случайно в main local.

**Rubric:** Создать branch at commit; безопасно restore main.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Practical Git scenarios**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
