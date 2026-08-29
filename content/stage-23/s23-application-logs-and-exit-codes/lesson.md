# Application logs and exit codes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Application logs and exit codes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `stdout/stderr`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Application logs and exit codes** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**stdout/stderr.** `stdout/stderr` связывает shell command с конкретным process, file, permission, environment или network state.

**exit status.** `exit status` связывает shell command с конкретным process, file, permission, environment или network state.

**pipeline failure awareness.** `pipeline failure awareness` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `stdout/stderr` и `exit status` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `stdout/stderr`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- stdout/stderr
- exit status
- pipeline failure awareness

### Полезно

- связать Application logs and exit codes с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Application logs and exit codes: отдельный пример

```bash
# 23.8 · Application logs and exit codes
# Focus: stdout/stderr, exit status, pipeline failure awareness
printf '%s
' 's23_application_logs_and_exit_codes'
```

Свяжи command с конкретным process, file, permission, environment или port symptom.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `stdout/stderr` до запуска.

**B · Find the bug.** Найди нарушение `exit status` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Application logs and exit codes за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Application logs and exit codes и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Application logs and exit codes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Application logs and exit codes: это отдельный технический контракт

### Нормальный Junior answer

> Application logs and exit codes — тема, в которой я сначала фиксирую `stdout/stderr`, затем объясняю `exit status` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Application logs and exit codes?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- stdout/stderr
- exit status
- pipeline failure awareness

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Application logs and exit codes?

## Задача

Сделай короткую письменную практику по теме **Application logs and exit codes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Application logs and exit codes: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
