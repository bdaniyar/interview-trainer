# ORDER BY, LIMIT and OFFSET

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **ORDER BY, LIMIT and OFFSET**, а не только запомнить термин;
- прочитать и изменить короткий пример для `deterministic ordering`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`ORDER BY` defines result order; `LIMIT` bounds rows and `OFFSET` skips rows for simple pagination.

### Как работает

Multiple order columns are evaluated left to right. A unique tie-breaker such as id is needed for deterministic pages when primary sort values tie.


### Важный нюанс / limitation

Large OFFSET makes the database scan/discard earlier rows and concurrent inserts can shift page boundaries; keyset pagination scales better.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- deterministic ordering
- multi-column ordering
- pagination caveats

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### ORDER BY, LIMIT and OFFSET: отдельный пример

```sql
SELECT id, created_at
FROM events
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 20;
```

Уникальный `id` — tie-breaker: страницы остаются детерминированными при одинаковом времени.

## Common mistakes

### Ошибка 1

Using LIMIT/OFFSET without a stable unique ordering returns duplicated or missing rows across pages.

## Practice

**A · Code/result prediction.** Change one input in the `deterministic ordering` example and predict the result before running it.

**B · Find the bug.** Find code that violates `multi-column ordering` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `deterministic ordering` and add one edge-case test.

**E · Interview explanation.** Explain ORDER BY, LIMIT and OFFSET in 45–60 seconds and include one limitation.

## SQL practice

### Последние два заказа

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

**Вопрос:** Верни два последних заказа по created_at, при равенстве — больший id первым.

Expected columns: id, created_at. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Вторая страница

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

**Вопрос:** Верни вторую страницу пользователей размера 2 с устойчивым order по id.

Expected columns: id, email. Comparison: ordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### Missing deterministic order

**Сценарий:** LIMIT 20 иногда возвращает другой набор строк.

**Rubric:** Добавить ORDER BY с уникальным tie-breaker; без него SQL не обещает порядок.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое ORDER BY, LIMIT and OFFSET и как это работает?

### Follow-up

Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`ORDER BY` defines result order; `LIMIT` bounds rows and `OFFSET` skips rows for simple pagination.

### Нормальный Junior answer

> `ORDER BY` defines result order; `LIMIT` bounds rows and `OFFSET` skips rows for simple pagination. Multiple order columns are evaluated left to right. A unique tie-breaker such as id is needed for deterministic pages when primary sort values tie. Важное ограничение: Large OFFSET makes the database scan/discard earlier rows and concurrent inserts can shift page boundaries; keyset pagination scales better.

### Углубление / follow-up

**Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?**

Using LIMIT/OFFSET without a stable unique ordering returns duplicated or missing rows across pages.

## Expected answer rubric

### Must mention

- deterministic ordering
- multi-column ordering
- pagination caveats

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using LIMIT/OFFSET without a stable unique ordering returns duplicated or missing rows across pages.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?

## Задача

Сделай короткую письменную практику по теме **ORDER BY, LIMIT and OFFSET**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `ORDER BY` defines result order; `LIMIT` bounds rows and `OFFSET` skips rows for simple pagination.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Using LIMIT/OFFSET without a stable unique ordering returns duplicated or missing rows across pages.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
