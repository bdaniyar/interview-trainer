# File operations

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **File operations**, а не только запомнить термин;
- прочитать и изменить короткий пример для `mkdir`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **File operations** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**mkdir.** `mkdir` связывает shell command с конкретным process, file, permission, environment или network state.

**cp.** `cp` связывает shell command с конкретным process, file, permission, environment или network state.

**mv.** `mv` связывает shell command с конкретным process, file, permission, environment или network state.

**rm.** `rm` связывает shell command с конкретным process, file, permission, environment или network state.

**safe destructive operations.** `safe destructive operations` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `mkdir` и `cp` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `mkdir`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- mkdir
- cp
- mv
- rm

### Полезно

- safe destructive operations

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### File operations: отдельный пример

```bash
# 23.2 · File operations
# Focus: mkdir, cp, mv, rm
printf '%s
' 's23_file_operations'
```

Свяжи command с конкретным process, file, permission, environment или port symptom.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `mkdir` до запуска.

**B · Find the bug.** Найди нарушение `cp` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про File operations за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое File operations и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме File operations?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

File operations: это отдельный технический контракт

### Нормальный Junior answer

> File operations — тема, в которой я сначала фиксирую `mkdir`, затем объясняю `cp` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме File operations?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- mkdir
- cp
- mv
- rm

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме File operations?

## Задача

Сделай короткую письменную практику по теме **File operations**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** File operations: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
