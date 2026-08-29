# SELECT, aliases and expressions

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **SELECT, aliases and expressions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `selecting columns`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`SELECT` chooses result columns or expressions; aliases name output fields without changing stored schema.

### Как работает

Expressions are evaluated for rows produced by FROM/JOIN/filter/group stages. `SELECT *` couples callers to schema changes and transfers unused data.


### Важный нюанс / limitation

SQL result order is undefined without `ORDER BY`, even when a local test appears stable.

### Где используется в backend

API repositories project only fields needed for response DTOs.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- selecting columns
- computed fields
- aliases
- readable formatting

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### SELECT, aliases and expressions: отдельный пример

```sql
SELECT
    id AS product_id,
    price,
    price * 1.12 AS price_with_tax
FROM products;
```

SELECT формирует projection: alias меняет имя result column, expression вычисляется для каждой строки.

## Common mistakes

### Ошибка 1

Relying on implicit row order or ambiguous duplicate column names makes pagination and mapping unstable.

## Practice

**A · Code/result prediction.** Change one input in the `selecting columns` example and predict the result before running it.

**B · Find the bug.** Find code that violates `computed fields` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `selecting columns` and add one edge-case test.

**E · Interview explanation.** Explain SELECT, aliases and expressions in 45–60 seconds and include one limitation.

## SQL practice

### Активные пользователи

```sql
CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text NOT NULL UNIQUE,
    country text,
    active boolean NOT NULL DEFAULT true,
    manager_id bigint REFERENCES users(id),
    created_at timestamptz NOT NULL
);
CREATE TABLE orders (
    id bigint PRIMARY KEY,
    user_id bigint NOT NULL REFERENCES users(id),
    status text NOT NULL,
    total numeric(12, 2) NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE TABLE products (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    category text NOT NULL,
    price numeric(12, 2) NOT NULL
);
CREATE TABLE order_items (
    order_id bigint REFERENCES orders(id),
    product_id bigint REFERENCES products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);
```

Seed:

```sql
INSERT INTO users VALUES
(1,'a@example.com','KZ',true,NULL,'2026-01-01'),
(2,'b@example.com','KZ',true,1,'2026-01-02'),
(3,'c@example.com',NULL,false,1,'2026-01-03'),
(4,'d@example.com','GE',true,2,'2026-01-04');
INSERT INTO orders VALUES
(10,1,'paid',100,'2026-02-01'), (11,1,'cancelled',40,'2026-02-02'),
(12,2,'paid',200,'2026-02-03'), (13,2,'paid',50,'2026-02-04'),
(14,4,'new',80,'2026-02-05');
INSERT INTO products VALUES
(100,'Python Book','books',30), (101,'Keyboard','hardware',90), (102,'SQL Book','books',40);
INSERT INTO order_items VALUES (10,100,2),(10,101,1),(12,101,2),(13,102,1),(14,100,1);
```

**Вопрос:** Выбери id и email активных пользователей.

Expected columns: id, email. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое SELECT, aliases and expressions и как это работает?

### Follow-up

Какая типичная ошибка связана с SELECT, aliases and expressions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`SELECT` chooses result columns or expressions; aliases name output fields without changing stored schema.

### Нормальный Junior answer

> `SELECT` chooses result columns or expressions; aliases name output fields without changing stored schema. Expressions are evaluated for rows produced by FROM/JOIN/filter/group stages. `SELECT *` couples callers to schema changes and transfers unused data. Важное ограничение: SQL result order is undefined without `ORDER BY`, even when a local test appears stable.

### Углубление / follow-up

**Какая типичная ошибка связана с SELECT, aliases and expressions?**

Relying on implicit row order or ambiguous duplicate column names makes pagination and mapping unstable.

## Expected answer rubric

### Must mention

- selecting columns
- computed fields
- aliases
- readable formatting

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Relying on implicit row order or ambiguous duplicate column names makes pagination and mapping unstable.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с SELECT, aliases and expressions?

## Задача

Сделай короткую письменную практику по теме **SELECT, aliases and expressions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `SELECT` chooses result columns or expressions; aliases name output fields without changing stored schema.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Relying on implicit row order or ambiguous duplicate column names makes pagination and mapping unstable.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
