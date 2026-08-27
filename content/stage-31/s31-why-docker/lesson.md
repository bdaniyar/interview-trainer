# Why Docker?

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- объяснить `reproducible environment` своими словами и связать с backend-сценарием;
- объяснить `dependency isolation` своими словами и связать с backend-сценарием;
- объяснить `multi-service local setup` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Сильный screening answer коротко связывает опыт с ролью и подтверждается конкретным действием кандидата.

В теме **Why Docker?** важно уверенно объяснять следующие части:

### reproducible environment

Для `reproducible environment` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### dependency isolation

Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

### multi-service local setup

Для `multi-service local setup` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### not “Docker automatically scales”

Container запускает изолированный process из image; данные вне writable layer сохраняют в volume.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

Сформулируй минимальный пример из текущего проекта: один happy path, одна граница и одна ошибка. Не добавляй инфраструктуру, не относящуюся к механизму.

## Common mistakes

**Ошибка:** Читать заученный список технологий без результата и личного вклада.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Why Docker?** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- reproducible environment
- dependency isolation
- multi-service local setup
- not “Docker automatically scales”.
- Используй STAR для поведения и context → decision → trade-off → verification для техники.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Читать заученный список технологий без результата и личного вклада.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- reproducible environment
- dependency isolation
- multi-service local setup
- not “Docker automatically scales”.

## Задача

Разбери backend-сценарий: **Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Why Docker?**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
