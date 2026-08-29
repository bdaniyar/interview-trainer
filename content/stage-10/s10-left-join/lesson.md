# LEFT JOIN

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **LEFT JOIN**, а не только запомнить термин;
- прочитать и изменить короткий пример для `preserving left rows`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`LEFT JOIN` preserves every left row and fills right-side columns with NULL when no match exists.

### Как работает

Right-table filters in ON affect which matches attach; the same filter in WHERE can remove NULL-extended rows and effectively turn the result into INNER JOIN.


### Важный нюанс / limitation

Count a nullable right primary key, not `COUNT(*)`, when measuring related rows per left entity.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- preserving left rows
- condition in `ON` vs `WHERE`
- finding missing related rows

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### LEFT JOIN: отдельный пример

```sql
SELECT u.id, COUNT(s.id) AS active_sessions
FROM users AS u
LEFT JOIN sessions AS s
  ON s.user_id = u.id AND s.revoked_at IS NULL
GROUP BY u.id;
```

Условие правой таблицы находится в ON, поэтому users без active sessions не исчезают.

## Common mistakes

### Ошибка 1

Putting `right.active = true` in WHERE unexpectedly removes left rows with no active relation.

## Practice

**A · Code/result prediction.** Change one input in the `preserving left rows` example and predict the result before running it.

**B · Find the bug.** Find code that violates `condition in `ON` vs `WHERE`` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `preserving left rows` and add one edge-case test.

**E · Interview explanation.** Explain LEFT JOIN in 45–60 seconds and include one limitation.

## SQL practice

### Пользователи без заказов

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

**Вопрос:** LEFT JOIN и найди users без orders.

Expected columns: id, email. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### LEFT JOIN с условием в ON

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

**Вопрос:** Верни всех users и id только paid orders, не теряя users без paid-заказов.

Expected columns: user_id, order_id. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Категории без продаж

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

**Вопрос:** Верни products, которые ни разу не встречались в order_items.

Expected columns: id, name. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### LEFT becomes INNER

**Сценарий:** WHERE right.status='paid' удалил NULL rows.

**Rubric:** Условие правой таблицы в ON или explicit NULL semantics.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое LEFT JOIN и как это работает?

### Follow-up

Какая типичная ошибка связана с LEFT JOIN?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`LEFT JOIN` preserves every left row and fills right-side columns with NULL when no match exists.

### Нормальный Junior answer

> `LEFT JOIN` preserves every left row and fills right-side columns with NULL when no match exists. Right-table filters in ON affect which matches attach; the same filter in WHERE can remove NULL-extended rows and effectively turn the result into INNER JOIN. Важное ограничение: Count a nullable right primary key, not `COUNT(*)`, when measuring related rows per left entity.

### Углубление / follow-up

**Какая типичная ошибка связана с LEFT JOIN?**

Putting `right.active = true` in WHERE unexpectedly removes left rows with no active relation.

## Expected answer rubric

### Must mention

- preserving left rows
- condition in `ON` vs `WHERE`
- finding missing related rows

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Putting `right.active = true` in WHERE unexpectedly removes left rows with no active relation.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с LEFT JOIN?

## Задача

Сделай короткую письменную практику по теме **LEFT JOIN**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `LEFT JOIN` preserves every left row and fills right-side columns with NULL when no match exists.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Putting `right.active = true` in WHERE unexpectedly removes left rows with no active relation.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
