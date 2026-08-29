# Window functions

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Window functions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `rows remain visible`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A window function computes across related rows while keeping each original row visible, unlike GROUP BY.

### Как работает

`OVER` defines partition, order and frame. Ranking, running totals and comparisons to previous rows are common uses.


### Важный нюанс / limitation

Ordering inside OVER controls the window calculation; final output order still requires a separate ORDER BY.

### Где используется в backend

Reports can add per-customer running totals without losing individual transactions.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- rows remain visible
- difference from GROUP BY
- window definition

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Window functions: отдельный пример

```sql
SELECT id, account_id, amount,
       SUM(amount) OVER (
           PARTITION BY account_id
           ORDER BY created_at, id
       ) AS running_balance
FROM ledger_entries;
```

Window aggregate сохраняет каждую ledger row и добавляет накопительный итог в пределах account.

## Common mistakes

### Ошибка 1

Omitting a tie-breaker from window ordering can make row_number results nondeterministic.

## Practice

**A · Code/result prediction.** Change one input in the `rows remain visible` example and predict the result before running it.

**B · Find the bug.** Find code that violates `difference from GROUP BY` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `rows remain visible` and add one edge-case test.

**E · Interview explanation.** Explain Window functions in 45–60 seconds and include one limitation.

## SQL practice

### Предыдущий order total

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

**Вопрос:** Добавь previous_total через LAG в рамках user.

Expected columns: id, user_id, total, previous_total. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Следующий order time

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

**Вопрос:** Добавь next_created_at через LEAD в рамках user.

Expected columns: id, user_id, next_created_at. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое Window functions и как это работает?

### Follow-up

Какая типичная ошибка связана с Window functions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A window function computes across related rows while keeping each original row visible, unlike GROUP BY.

### Нормальный Junior answer

> A window function computes across related rows while keeping each original row visible, unlike GROUP BY. `OVER` defines partition, order and frame. Ranking, running totals and comparisons to previous rows are common uses. Важное ограничение: Ordering inside OVER controls the window calculation; final output order still requires a separate ORDER BY.

### Углубление / follow-up

**Какая типичная ошибка связана с Window functions?**

Omitting a tie-breaker from window ordering can make row_number results nondeterministic.

## Expected answer rubric

### Must mention

- rows remain visible
- difference from GROUP BY
- window definition

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Omitting a tie-breaker from window ordering can make row_number results nondeterministic.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Window functions?

## Задача

Сделай короткую письменную практику по теме **Window functions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A window function computes across related rows while keeping each original row visible, unlike GROUP BY.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Omitting a tie-breaker from window ordering can make row_number results nondeterministic.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
