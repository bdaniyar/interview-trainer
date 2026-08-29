# Application logs and exit codes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- объяснить `stdout/stderr` своими словами и связать с backend-сценарием;
- объяснить `exit status` своими словами и связать с backend-сценарием;
- объяснить `pipeline failure awareness.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Linux basics нужны для запуска процесса, чтения логов, environment и диагностики ports/permissions.

В теме **Application logs and exit codes** важно уверенно объяснять следующие части:

### stdout/stderr

Для `stdout/stderr` свяжи command с конкретным process, file, permission, environment или network symptom.

### exit status

Для `exit status` свяжи command с конкретным process, file, permission, environment или network symptom.

### pipeline failure awareness

Для `pipeline failure awareness` свяжи command с конкретным process, file, permission, environment или network symptom.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

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

**Ошибка:** Менять permissions на 777 вместо поиска владельца и требуемого доступа.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Application logs and exit codes** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди процесс, его exit code, порт, env и последнюю ошибку в log. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- stdout/stderr
- exit status
- pipeline failure awareness.
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

- stdout/stderr
- exit status
- pipeline failure awareness.

## Задача

Разбери backend-сценарий: **Найди процесс, его exit code, порт, env и последнюю ошибку в log.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Application logs and exit codes**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
