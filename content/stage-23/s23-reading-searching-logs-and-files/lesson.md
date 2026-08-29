# Reading/searching logs and files

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Reading/searching logs and files**, а не только запомнить термин;
- прочитать и изменить короткий пример для `cat`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Reading/searching logs and files** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**cat.** `cat` связывает shell command с конкретным process, file, permission, environment или network state.

**less.** `less` связывает shell command с конкретным process, file, permission, environment или network state.

**head.** `head` связывает shell command с конкретным process, file, permission, environment или network state.

**tail.** `tail` связывает shell command с конкретным process, file, permission, environment или network state.

**grep/rg.** `grep/rg` связывает shell command с конкретным process, file, permission, environment или network state.

**`tail -f`.** ``tail -f`` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `cat` и `less` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `cat`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- cat
- less
- head
- tail

### Полезно

- grep/rg
- `tail -f`

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Reading/searching logs and files: отдельный пример

```text
Сценарий: Найди ERROR request_id=abc.

Проверка:
rg/grep + tail/context.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `cat` до запуска.

**B · Find the bug.** Найди нарушение `less` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Reading/searching logs and files за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Find error

**Сценарий:** Найди ERROR request_id=abc.

**Rubric:** rg/grep + tail/context.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Reading/searching logs and files и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Reading/searching logs and files?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Reading/searching logs and files: это отдельный технический контракт

### Нормальный Junior answer

> Reading/searching logs and files — тема, в которой я сначала фиксирую `cat`, затем объясняю `less` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Reading/searching logs and files?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- cat
- less
- head
- tail

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Reading/searching logs and files?

## Задача

Сделай короткую письменную практику по теме **Reading/searching logs and files**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Reading/searching logs and files: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
