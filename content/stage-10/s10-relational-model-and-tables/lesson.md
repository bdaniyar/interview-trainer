# Relational model and tables

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Relational model and tables**, а не только запомнить термин;
- прочитать и изменить короткий пример для `row`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Как работает

Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.

**row.** `row` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**column.** `column` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**relation.** `relation` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**schema.** `schema` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**data types.** `data types` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**relational thinking.** `relational thinking` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `row` и `column` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `row`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- row
- column
- relation
- schema

### Полезно

- data types
- relational thinking

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Relational model and tables: отдельный пример

```sql
CREATE TABLE authors (
    id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE articles (
    id bigint PRIMARY KEY,
    author_id bigint NOT NULL REFERENCES authors(id),
    title text NOT NULL
);
```

Таблицы моделируют сущности, primary key идентифицирует строку, foreign key хранит допустимую связь.

## Common mistakes

### Ошибка 1

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `row` до запуска.

**B · Find the bug.** Найди нарушение `column` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Relational model and tables за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Relational model and tables и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Relational model and tables?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Relational model and tables: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Нормальный Junior answer

> Relational model and tables — тема, в которой я сначала фиксирую `row`, затем объясняю `column` на коротком примере. Ключевой механизм: Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа. Главная практическая ошибка — Не определить cardinality результата и замаскировать неверный query через DISTINCT.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Relational model and tables?**

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Expected answer rubric

### Must mention

- row
- column
- relation
- schema

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Relational model and tables?

## Задача

Сделай короткую письменную практику по теме **Relational model and tables**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Relational model and tables: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
