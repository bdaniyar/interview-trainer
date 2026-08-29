# Selectivity

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Selectivity**, а не только запомнить термин;
- прочитать и изменить короткий пример для `low-cardinality fields`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**low-cardinality fields.** `low-cardinality fields` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**why planner may prefer sequential scan.** `why planner may prefer sequential scan` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `low-cardinality fields` и `why planner may prefer sequential scan` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `low-cardinality fields`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- low-cardinality fields
- why planner may prefer sequential scan

### Полезно

- связать Selectivity с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Selectivity: отдельный пример

```sql
-- 11.7 · Selectivity
-- Focus: low-cardinality fields, why planner may prefer sequential scan
SELECT 's11_selectivity' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `low-cardinality fields` до запуска.

**B · Find the bug.** Найди нарушение `why planner may prefer sequential scan` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Selectivity за 60 секунд: определение, механизм, пример, ограничение.

## SQL practice

### Covering index

```sql
CREATE TABLE rooms (
    id bigint PRIMARY KEY,
    hotel_id bigint NOT NULL,
    number text NOT NULL,
    UNIQUE (hotel_id, number)
);
CREATE TABLE bookings (
    id bigint PRIMARY KEY,
    room_id bigint NOT NULL REFERENCES rooms(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL,
    CHECK (ends_at > starts_at)
);
```

Seed:

```sql
INSERT INTO rooms VALUES (1,10,'101'),(2,10,'102');
INSERT INTO bookings VALUES
(1,1,'2026-09-01','2026-09-05','confirmed'),
(2,1,'2026-09-10','2026-09-12','cancelled');
```

**Вопрос:** Query фильтрует user_id, сортирует created_at и возвращает total. Когда уместен INCLUDE?

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое Selectivity и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Selectivity?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Selectivity: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный Junior answer

> Selectivity — тема, в которой я сначала фиксирую `low-cardinality fields`, затем объясняю `why planner may prefer sequential scan` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Selectivity?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Expected answer rubric

### Must mention

- low-cardinality fields
- why planner may prefer sequential scan

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Selectivity?

## Задача

Сделай короткую письменную практику по теме **Selectivity**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Selectivity: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
