# WHERE and boolean logic

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **WHERE and boolean logic**, а не только запомнить термин;
- прочитать и изменить короткий пример для `comparisons`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`WHERE` filters source rows using boolean predicates before grouping and aggregation.

### Как работает

AND binds tighter than OR, so parentheses make intended logic explicit. NULL comparisons yield UNKNOWN and require `IS NULL`/`IS NOT NULL`.


### Важный нюанс / limitation

Functions applied to an indexed column can prevent a simple index access path; confirm with EXPLAIN rather than guessing.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- comparisons
- AND/OR/NOT
- parentheses
- ranges

### Полезно

- pattern matching

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### WHERE and boolean logic: отдельный пример

```sql
SELECT id, email
FROM users
WHERE active IS TRUE
  AND created_at >= DATE '2026-01-01';
```

WHERE оставляет только строки, для которых всё boolean expression истинно.

## Common mistakes

### Ошибка 1

`status = 'paid' OR status = 'new' AND active` usually means something different from the visually assumed grouping.

## Practice

**A · Code/result prediction.** Change one input in the `comparisons` example and predict the result before running it.

**B · Find the bug.** Find code that violates `AND/OR/NOT` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `comparisons` and add one edge-case test.

**E · Interview explanation.** Explain WHERE and boolean logic in 45–60 seconds and include one limitation.

## SQL practice

### Email domain

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

**Вопрос:** Найди email, заканчивающиеся на @example.com.

Expected columns: email. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Пользователи после даты

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

**Вопрос:** Выбери id пользователей, созданных не раньше 2026-01-03.

Expected columns: id. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое WHERE and boolean logic и как это работает?

### Follow-up

Какая типичная ошибка связана с WHERE and boolean logic?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`WHERE` filters source rows using boolean predicates before grouping and aggregation.

### Нормальный Junior answer

> `WHERE` filters source rows using boolean predicates before grouping and aggregation. AND binds tighter than OR, so parentheses make intended logic explicit. NULL comparisons yield UNKNOWN and require `IS NULL`/`IS NOT NULL`. Важное ограничение: Functions applied to an indexed column can prevent a simple index access path; confirm with EXPLAIN rather than guessing.

### Углубление / follow-up

**Какая типичная ошибка связана с WHERE and boolean logic?**

`status = 'paid' OR status = 'new' AND active` usually means something different from the visually assumed grouping.

## Expected answer rubric

### Must mention

- comparisons
- AND/OR/NOT
- parentheses
- ranges

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- `status = 'paid' OR status = 'new' AND active` usually means something different from the visually assumed grouping.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с WHERE and boolean logic?

## Задача

Сделай короткую письменную практику по теме **WHERE and boolean logic**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `WHERE` filters source rows using boolean predicates before grouping and aggregation.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** `status = 'paid' OR status = 'new' AND active` usually means something different from the visually assumed grouping.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
