# Environment variables

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- объяснить `export` своими словами и связать с backend-сценарием;
- объяснить `process inheritance` своими словами и связать с backend-сценарием;
- объяснить `quoting` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Linux basics нужны для запуска процесса, чтения логов, environment и диагностики ports/permissions.

В теме **Environment variables** важно уверенно объяснять следующие части:

### export

Для `export` свяжи command с конкретным process, file, permission, environment или network symptom.

### process inheritance

Inheritance выражает отношение is-a и участвует в MRO; если нужно только переиспользовать collaborator, composition обычно делает зависимость яснее.

### quoting

Для `quoting` свяжи command с конкретным process, file, permission, environment или network symptom.

### secrets

Для `secrets` свяжи command с конкретным process, file, permission, environment или network symptom.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```bash
ps aux | rg uvicorn
ss -ltnp | rg 8000
tail -n 100 /var/log/app.log
printf '%s\n' "$APP_ENV"
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Менять permissions на 777 вместо поиска владельца и требуемого доступа.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Environment variables** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Найди процесс, его exit code, порт, env и последнюю ошибку в log. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- export
- process inheritance
- quoting
- secrets.
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

- export
- process inheritance
- quoting
- secrets.

## Задача

Разбери backend-сценарий: **Найди процесс, его exit code, порт, env и последнюю ошибку в log.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Operations practice

### Missing env

**Сценарий:** Local works, service KeyError APP_ENV.

**Rubric:** Runtime env source, quoting, restart.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Environment variables**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
