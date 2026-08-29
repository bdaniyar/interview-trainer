# Subqueries

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Subqueries**, а не только запомнить термин;
- прочитать и изменить короткий пример для `scalar`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A subquery is a query used as an expression or table source inside another statement.

### Как работает

A scalar subquery must return at most one row; `IN` compares against a set of values; a FROM subquery exposes a derived table with an alias.


### Важный нюанс / limitation

Prefer the form that expresses intent clearly. Performance depends on the planner and data, not a universal 'JOIN is faster' rule.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- scalar
- table subquery
- `IN`
- nested aggregation

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Subqueries: отдельный пример

```sql
SELECT id, total
FROM invoices
WHERE total > (SELECT AVG(total) FROM invoices);
```

Scalar subquery вычисляет среднее один раз для сравнения каждой invoice.

## Common mistakes

### Ошибка 1

A scalar subquery returning multiple rows raises an error; `NOT IN` with NULL can also produce surprising UNKNOWN results.

## Practice

**A · Code/result prediction.** Change one input in the `scalar` example and predict the result before running it.

**B · Find the bug.** Find code that violates `table subquery` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `scalar` and add one edge-case test.

**E · Interview explanation.** Explain Subqueries in 45–60 seconds and include one limitation.

## SQL practice

### Заказы выше среднего

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

**Вопрос:** Найди orders с total выше среднего total всех orders.

Expected columns: id, total. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое Subqueries и как это работает?

### Follow-up

Какая типичная ошибка связана с Subqueries?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A subquery is a query used as an expression or table source inside another statement.

### Нормальный Junior answer

> A subquery is a query used as an expression or table source inside another statement. A scalar subquery must return at most one row; `IN` compares against a set of values; a FROM subquery exposes a derived table with an alias. Важное ограничение: Prefer the form that expresses intent clearly. Performance depends on the planner and data, not a universal 'JOIN is faster' rule.

### Углубление / follow-up

**Какая типичная ошибка связана с Subqueries?**

A scalar subquery returning multiple rows raises an error; `NOT IN` with NULL can also produce surprising UNKNOWN results.

## Expected answer rubric

### Must mention

- scalar
- table subquery
- `IN`
- nested aggregation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- A scalar subquery returning multiple rows raises an error; `NOT IN` with NULL can also produce surprising UNKNOWN results.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Subqueries?

## Задача

Сделай короткую письменную практику по теме **Subqueries**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A subquery is a query used as an expression or table source inside another statement.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** A scalar subquery returning multiple rows raises an error; `NOT IN` with NULL can also produce surprising UNKNOWN results.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
