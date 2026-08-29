# Repository, working tree, index and commit

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `Repository, working tree, index and commit` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Git хранит snapshots и граф commits; working tree, index, local branch и remote-tracking branch — разные состояния.

В теме **Repository, working tree, index and commit** важно уверенно объяснять следующие части:

### Repository, working tree, index and commit

Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Repository, working tree, index and commit: отдельный пример

```bash
# 22.1 · Repository, working tree, index and commit
# Focus: Repository, working tree, index and commit
printf '%s
' 's22_repository_working_tree_index_and_commit'
```

Перед командой назови изменяемое состояние: files, index, branch pointer или shared history.

## Common mistakes

**Ошибка:** Rebase shared commits или удалять secret из файла без ротации.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Repository, working tree, index and commit** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери безопасный способ отменить локальное и уже опубликованное изменение. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- Repository, working tree, index and commit
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

- Repository, working tree, index and commit

## Задача

Разбери backend-сценарий: **Выбери безопасный способ отменить локальное и уже опубликованное изменение.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Repository, working tree, index and commit**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
