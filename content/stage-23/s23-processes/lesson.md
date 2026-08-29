# Processes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- объяснить `ps` своими словами и связать с backend-сценарием;
- объяснить `foreground/background` своими словами и связать с backend-сценарием;
- объяснить `signals` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Linux basics нужны для запуска процесса, чтения логов, environment и диагностики ports/permissions.

В теме **Processes** важно уверенно объяснять следующие части:

### ps

Для `ps` свяжи command с конкретным process, file, permission, environment или network symptom.

### foreground/background

Для `foreground/background` свяжи command с конкретным process, file, permission, environment или network symptom.

### signals

Для `signals` свяжи command с конкретным process, file, permission, environment или network symptom.

### kill

Для `kill` свяжи command с конкретным process, file, permission, environment или network symptom.

### graceful termination

Для `graceful termination` свяжи command с конкретным process, file, permission, environment или network symptom.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Processes: отдельный пример

```text
Сценарий: Uvicorn сразу code 1.

Проверка:
stderr/log, command, env, permissions, port.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Менять permissions на 777 вместо поиска владельца и требуемого доступа.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Processes** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди процесс, его exit code, порт, env и последнюю ошибку в log. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- ps
- foreground/background
- signals
- kill
- Процесс видит filesystem, env, user permissions, descriptors и network namespace.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Менять permissions на 777 вместо поиска владельца и требуемого доступа.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- ps
- foreground/background
- signals
- kill
- graceful termination.

## Задача

Разбери backend-сценарий: **Найди процесс, его exit code, порт, env и последнюю ошибку в log.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Operations practice

### Process exit

**Сценарий:** Uvicorn сразу code 1.

**Rubric:** stderr/log, command, env, permissions, port.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Processes**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
