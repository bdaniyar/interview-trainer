# Conflict resolution

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `markers` своими словами и связать с backend-сценарием;
- объяснить `understand both sides` своими словами и связать с backend-сценарием;
- объяснить `test after resolution` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Git хранит snapshots и граф commits; working tree, index, local branch и remote-tracking branch — разные состояния.

В теме **Conflict resolution** важно уверенно объяснять следующие части:

### markers

Для `markers` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### understand both sides

Для `understand both sides` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### test after resolution

Для `test after resolution` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

### continue/abort

Для `continue/abort` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Conflict resolution: отдельный пример

```text
Сценарий: Markers удалены, tests не запускались.

Проверка:
Понять обе стороны, stage, test.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Rebase shared commits или удалять secret из файла без ротации.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Conflict resolution** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери безопасный способ отменить локальное и уже опубликованное изменение. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- markers
- understand both sides
- test after resolution
- continue/abort.
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

- markers
- understand both sides
- test after resolution
- continue/abort.

## Задача

Разбери backend-сценарий: **Выбери безопасный способ отменить локальное и уже опубликованное изменение.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

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

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Conflict resolution**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
