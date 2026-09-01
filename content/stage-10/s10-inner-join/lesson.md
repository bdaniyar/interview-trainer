# INNER JOIN

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **INNER JOIN**, а не только запомнить термин;
- прочитать и изменить короткий пример для `join condition`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`INNER JOIN` соединяет строки двух источников по условию и оставляет только совпавшие пары. Строка без пары с любой стороны в результат не попадёт.

### Как работает

Сначала формируются пары, для которых выражение `ON` истинно. Связь one-to-many размножает строку стороны one: один user с тремя orders даст три result rows. После JOIN применяются WHERE, grouping и projection.


### Пример

```sql
SELECT o.id AS order_id, u.email
FROM orders AS o
JOIN users AS u ON u.id = o.user_id
ORDER BY o.id;
```

| order_id | email |
|---:|---|
| 10 | a@example.com |
| 11 | a@example.com |
| 12 | b@example.com |

### Важный нюанс / ограничение

JOIN не устраняет duplicates. Если условие отсутствует или неполное, появляется Cartesian multiplication. `DISTINCT` может скрыть ошибку cardinality, но не исправляет неверную связь. Всегда определяй grain результата.

### Где используется в backend

Типичный запрос связывает `orders.user_id` с `users.id`, чтобы вернуть заказ и email владельца одним result set.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- условие ON
- только matched rows
- one-to-many cardinality
- Cartesian product

### Полезно

- aliases
- оценка grain
- проверка FK/index по join key

### Можно не учить глубоко

- внутренние алгоритмы hash/merge/nested-loop join до чтения EXPLAIN

## Примеры кода

### INNER JOIN: отдельный пример

```sql
SELECT a.id, a.title, u.email AS author_email
FROM articles AS a
JOIN users AS u ON u.id = a.author_id
ORDER BY a.id;
```

INNER JOIN оставляет только пары строк, удовлетворяющие условию связи author_id → users.id.

## Типичные ошибки

### Ошибка 1

Забыть `ON` или часть composite key и получить резкий рост числа строк.

### Ошибка 2

Добавить `DISTINCT` вместо проверки one-to-many cardinality.

### Ошибка 3

Выбрать INNER JOIN, когда бизнес-требование должно сохранить users без orders.

## Практика

**A · Result предсказание результата.** По двум маленьким таблицам посчитай число result rows вручную.

**B · Найди ошибку.** Найди отсутствующее условие JOIN.

**C · Улучшение кода.** Замени correlated lookup понятным JOIN, не меняя cardinality.

**D · SQL task.** Верни `order_id` и email владельца заказа.

## Практика SQL

### Пользователь каждого заказа

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

Начальные данные:

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

**Вопрос:** INNER JOIN orders/users; верни order_id и email.

Ожидаемые столбцы: order_id, email. Сравнение: без учёта порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

### Товары заказа

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

Начальные данные:

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

**Вопрос:** Для order 10 верни product name и quantity.

Ожидаемые столбцы: name, quantity. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

### Состав paid-заказов

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

Начальные данные:

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

**Вопрос:** Соедини users, orders, items, products; верни email, order_id, product и quantity для paid.

Ожидаемые столбцы: email, order_id, name, quantity. Сравнение: без учёта порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

### Количество товаров в заказе

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

Начальные данные:

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

**Вопрос:** Для каждого order с items верни сумму quantity.

Ожидаемые столбцы: id, units. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Wrong JOIN condition

**Сценарий:** JOIN orders/users размножил и сопоставил несвязанные строки.

**Критерии ответа:** Проверить foreign-key cardinality и ON u.id=o.user_id; сравнить row count до/после JOIN.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Как работает INNER JOIN и почему он может увеличить число строк?

### Дополнительный вопрос

Когда вместо INNER JOIN нужен LEFT JOIN?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

INNER JOIN оставляет пары, удовлетворяющие ON; one-to-many даёт несколько rows на одну строку стороны one.

### Нормальный ответ уровня Junior

> INNER JOIN объединяет только совпавшие строки по условию `ON`. Перед запросом я определяю grain: например, одна строка результата на order. Если у user несколько orders, user повторится для каждого заказа — это не SQL duplicate, а cardinality связи. Отсутствующее условие создаёт Cartesian product, и `DISTINCT` не должен маскировать такую ошибку.

### Углубление / дополнительный вопрос

**Когда вместо INNER JOIN нужен LEFT JOIN?**

Когда нужно сохранить все строки левой таблицы, включая те, для которых связь не найдена; поля правой стороны тогда будут NULL.

## Критерии хорошего ответа

### Что обязательно упомянуть

- условие ON
- только matched rows
- one-to-many cardinality
- Cartesian product

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Забыть `ON` или часть composite key и получить резкий рост числа строк.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Когда вместо INNER JOIN нужен LEFT JOIN?

## Задача

Сделай короткую письменную практику по теме **INNER JOIN**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** INNER JOIN оставляет пары, удовлетворяющие ON; one-to-many даёт несколько rows на одну строку стороны one.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Забыть `ON` или часть composite key и получить резкий рост числа строк.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
