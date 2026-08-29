# Set operations

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Set operations**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``UNION``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Как работает

Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.

**`UNION`.** ``UNION`` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**`UNION ALL`.** ``UNION ALL`` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**`INTERSECT`.** ``INTERSECT`` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**`EXCEPT`.** ``EXCEPT`` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``UNION`` и ``UNION ALL`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``UNION``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT`

### Полезно

- связать Set operations с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Set operations: отдельный пример

```sql
SELECT email FROM newsletter_subscribers
UNION
SELECT email FROM registered_users

INTERSECT
SELECT email FROM verified_emails;
```

Set operations требуют совместимых columns; UNION удаляет duplicates, INTERSECT оставляет общие строки.

## Common mistakes

### Ошибка 1

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``UNION`` до запуска.

**B · Find the bug.** Найди нарушение ``UNION ALL`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Set operations за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Set operations и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Set operations?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Set operations: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Нормальный Junior answer

> Set operations — тема, в которой я сначала фиксирую ``UNION``, затем объясняю ``UNION ALL`` на коротком примере. Ключевой механизм: Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа. Главная практическая ошибка — Не определить cardinality результата и замаскировать неверный query через DISTINCT.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Set operations?**

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Expected answer rubric

### Must mention

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Set operations?

## Задача

Сделай короткую письменную практику по теме **Set operations**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Set operations: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
