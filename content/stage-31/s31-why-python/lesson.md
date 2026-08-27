# Why Python?

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- объяснить `productivity` своими словами и связать с backend-сценарием;
- объяснить `ecosystem` своими словами и связать с backend-сценарием;
- объяснить `readability` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Сильный screening answer коротко связывает опыт с ролью и подтверждается конкретным действием кандидата.

В теме **Why Python?** важно уверенно объяснять следующие части:

### productivity

Для `productivity` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### ecosystem

Для `ecosystem` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### readability

Для `readability` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### trade-offs

Для `trade-offs` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### no “Python is always fastest/best”

Для `no “Python is always fastest/best”` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

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

1. Объясни **Why Python?** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- productivity
- ecosystem
- readability
- trade-offs
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

- productivity
- ecosystem
- readability
- trade-offs
- no “Python is always fastest/best”.

## Задача

Разбери backend-сценарий: **Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Why Python?**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
