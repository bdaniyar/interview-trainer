# Student schedule and availability

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- объяснить `honest availability` своими словами и связать с backend-сценарием;
- объяснить `part-time/flexible preference` своими словами и связать с backend-сценарием;
- объяснить `clear commitment` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Сильный screening answer коротко связывает опыт с ролью и подтверждается конкретным действием кандидата.

В теме **Student schedule and availability** важно уверенно объяснять следующие части:

### honest availability

Для `honest availability` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### part-time/flexible preference

Для `part-time/flexible preference` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### clear commitment

Для `clear commitment` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

### no promises impossible to combine with study

Для `no promises impossible to combine with study` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.

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

1. Объясни **Student schedule and availability** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- honest availability
- part-time/flexible preference
- clear commitment
- no promises impossible to combine with study.
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

- honest availability
- part-time/flexible preference
- clear commitment
- no promises impossible to combine with study.

## Задача

Разбери backend-сценарий: **Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Student schedule and availability**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
