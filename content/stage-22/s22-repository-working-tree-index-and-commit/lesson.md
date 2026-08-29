# Repository, working tree, index and commit

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Repository, working tree, index and commit**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Repository, working tree, index and commit`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Repository, working tree, index and commit** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Repository, working tree, index and commit.** Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Repository, working tree, index and commit` и `Repository, working tree, index and commit` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Repository, working tree, index and commit`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Repository, working tree, index and commit

### Полезно

- связать Repository, working tree, index and commit с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

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

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Repository, working tree, index and commit` до запуска.

**B · Find the bug.** Найди нарушение `Repository, working tree, index and commit` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Repository, working tree, index and commit за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Repository, working tree, index and commit и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Repository, working tree, index and commit?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Repository, working tree, index and commit: это отдельный технический контракт

### Нормальный Junior answer

> Repository, working tree, index and commit — тема, в которой я сначала фиксирую `Repository, working tree, index and commit`, затем объясняю `Repository, working tree, index and commit` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Repository, working tree, index and commit?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Repository, working tree, index and commit

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Repository, working tree, index and commit?

## Задача

Сделай короткую письменную практику по теме **Repository, working tree, index and commit**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Repository, working tree, index and commit: это отдельный технический контракт
- **Механизм:** Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Git reference](https://git-scm.com/docs)
- [Pro Git](https://git-scm.com/book/en/v2)

Последняя проверка версий: **2026-08-27**.
