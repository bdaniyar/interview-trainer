# Processes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Processes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `ps`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Processes** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**ps.** `ps` связывает shell command с конкретным process, file, permission, environment или network state.

**foreground/background.** `foreground/background` связывает shell command с конкретным process, file, permission, environment или network state.

**signals.** `signals` связывает shell command с конкретным process, file, permission, environment или network state.

**kill.** `kill` связывает shell command с конкретным process, file, permission, environment или network state.

**graceful termination.** `graceful termination` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `ps` и `foreground/background` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `ps`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- ps
- foreground/background
- signals
- kill

### Полезно

- graceful termination

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Processes: отдельный пример

```text
Сценарий: Uvicorn сразу code 1.

Проверка:
stderr/log, command, env, permissions, port.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `ps` до запуска.

**B · Find the bug.** Найди нарушение `foreground/background` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Processes за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Process exit

**Сценарий:** Uvicorn сразу code 1.

**Rubric:** stderr/log, command, env, permissions, port.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Processes и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Processes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Processes: это отдельный технический контракт

### Нормальный Junior answer

> Processes — тема, в которой я сначала фиксирую `ps`, затем объясняю `foreground/background` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Processes?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- ps
- foreground/background
- signals
- kill

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Processes?

## Задача

Сделай короткую письменную практику по теме **Processes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Processes: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
