# Data modification

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Data modification**, а не только запомнить термин;
- прочитать и изменить короткий пример для `INSERT`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Как работает

Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.

**INSERT.** `INSERT` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**UPDATE.** `UPDATE` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**DELETE.** `DELETE` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**`RETURNING`.** ``RETURNING`` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**safe WHERE.** `WHERE` фильтрует строки до grouping; SQL three-valued logic отбрасывает и `FALSE`, и `UNKNOWN`.

**upsert basics.** `upsert basics` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `INSERT` и `UPDATE` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `INSERT`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- INSERT
- UPDATE
- DELETE
- `RETURNING`

### Полезно

- safe WHERE
- upsert basics

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Data modification: отдельный пример

```sql
UPDATE jobs
SET status = 'running', started_at = now()
WHERE id = $1 AND status = 'queued'
RETURNING id, status, started_at;
```

Conditional UPDATE объединяет проверку текущего state и изменение; RETURNING отдаёт фактически обновлённую строку.

## Common mistakes

### Ошибка 1

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `INSERT` до запуска.

**B · Find the bug.** Найди нарушение `UPDATE` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Data modification за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Data modification и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Data modification?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Data modification: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Нормальный Junior answer

> Data modification — тема, в которой я сначала фиксирую `INSERT`, затем объясняю `UPDATE` на коротком примере. Ключевой механизм: Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа. Главная практическая ошибка — Не определить cardinality результата и замаскировать неверный query через DISTINCT.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Data modification?**

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Expected answer rubric

### Must mention

- INSERT
- UPDATE
- DELETE
- `RETURNING`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Data modification?

## Задача

Сделай короткую письменную практику по теме **Data modification**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Data modification: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
