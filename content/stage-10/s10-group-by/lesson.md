# GROUP BY

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **GROUP BY**, а не только запомнить термин;
- прочитать и изменить короткий пример для `grouping`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`GROUP BY` forms groups of rows and returns one result row per unique grouping key.

### Как работает

Aggregate functions compute inside each group. Selected non-aggregate columns must normally appear in GROUP BY or be functionally determined under DB rules.


### Важный нюанс / limitation

Always state the grain, such as one row per `user_id`, before adding joins that may multiply source rows.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- grouping
- selected non-aggregate columns
- common errors

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### GROUP BY: отдельный пример

```sql
SELECT customer_id, SUM(total) AS revenue
FROM invoices
WHERE paid_at IS NOT NULL
GROUP BY customer_id
ORDER BY customer_id;
```

GROUP BY задаёт grain «одна строка на customer», после чего SUM считает значение внутри каждой группы.

## Common mistakes

### Ошибка 1

Grouping after a one-to-many join can double-count totals if the join has a finer grain than the measure.

## Practice

**A · Code/result prediction.** Change one input in the `grouping` example and predict the result before running it.

**B · Find the bug.** Find code that violates `selected non-aggregate columns` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `grouping` and add one edge-case test.

**E · Interview explanation.** Explain GROUP BY in 45–60 seconds and include one limitation.

## SQL practice

### Заказы по status

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

**Вопрос:** Посчитай заказы по status и отсортируй status.

Expected columns: status, count. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Выручка по пользователю

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

**Вопрос:** Суммируй total только paid-заказов по user_id.

Expected columns: user_id, revenue. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Средний paid-чек

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

**Вопрос:** Найди средний total paid-заказа.

Expected columns: average_total. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### COUNT nullable

**Сценарий:** COUNT(country) меньше COUNT(*).

**Rubric:** COUNT(expression) пропускает NULL.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Incorrect GROUP BY

**Сценарий:** Запрос агрегирует по user_id, но выбирает произвольный email.

**Rubric:** Все неагрегированные columns должны быть функционально зависимы/в GROUP BY; сначала определить grain результата.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое GROUP BY и как это работает?

### Follow-up

Какая типичная ошибка связана с GROUP BY?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`GROUP BY` forms groups of rows and returns one result row per unique grouping key.

### Нормальный Junior answer

> `GROUP BY` forms groups of rows and returns one result row per unique grouping key. Aggregate functions compute inside each group. Selected non-aggregate columns must normally appear in GROUP BY or be functionally determined under DB rules. Важное ограничение: Always state the grain, such as one row per `user_id`, before adding joins that may multiply source rows.

### Углубление / follow-up

**Какая типичная ошибка связана с GROUP BY?**

Grouping after a one-to-many join can double-count totals if the join has a finer grain than the measure.

## Expected answer rubric

### Must mention

- grouping
- selected non-aggregate columns
- common errors

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Grouping after a one-to-many join can double-count totals if the join has a finer grain than the measure.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с GROUP BY?

## Задача

Сделай короткую письменную практику по теме **GROUP BY**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `GROUP BY` forms groups of rows and returns one result row per unique grouping key.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Grouping after a one-to-many join can double-count totals if the join has a finer grain than the measure.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
