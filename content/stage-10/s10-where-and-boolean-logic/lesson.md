# WHERE and boolean logic

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **WHERE and boolean logic**, а не только запомнить термин;
- прочитать и изменить короткий пример для `comparisons`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`WHERE` фильтрует исходные rows по boolean predicates до grouping и aggregation.

### Как работает

AND имеет более высокий приоритет, чем OR, поэтому parentheses фиксируют намерение. Сравнения с NULL дают UNKNOWN и требуют `IS NULL` или `IS NOT NULL`.


### Важный нюанс / ограничение

Функция вокруг indexed column может помешать простому index access path; решение проверяют через EXPLAIN.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- comparisons
- AND/OR/NOT
- parentheses
- ranges

### Полезно

- pattern matching

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### WHERE and boolean logic: отдельный пример

```sql
SELECT id, email
FROM users
WHERE active IS TRUE
  AND created_at >= DATE '2026-01-01';
```

WHERE оставляет только строки, для которых всё boolean expression истинно.

## Типичные ошибки

### Ошибка 1

`status = 'paid' OR status = 'new' AND active` часто означает не ту группировку, которую читатель предполагает визуально.

## Практика

**A · Предсказание результата.** Измени один input в примере `comparisons` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `AND/OR/NOT`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `comparisons`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни WHERE and boolean logic за 45–60 секунд и назови одно ограничение.

## Практика SQL

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

**Вопрос:** Найди email, заканчивающиеся на @example.com.

Ожидаемые столбцы: email. Сравнение: без учёта порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

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

**Вопрос:** Выбери id пользователей, созданных не раньше 2026-01-03.

Ожидаемые столбцы: id. Сравнение: без учёта порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое WHERE and boolean logic и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с WHERE and boolean logic?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`WHERE` фильтрует исходные rows по boolean predicates до grouping и aggregation.

### Нормальный ответ уровня Junior

> `WHERE` фильтрует исходные rows по boolean predicates до grouping и aggregation. AND имеет более высокий приоритет, чем OR, поэтому parentheses фиксируют намерение. Сравнения с NULL дают UNKNOWN и требуют `IS NULL` или `IS NOT NULL`. Важное ограничение: Функция вокруг indexed column может помешать простому index access path; решение проверяют через EXPLAIN.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с WHERE and boolean logic?**

`status = 'paid' OR status = 'new' AND active` часто означает не ту группировку, которую читатель предполагает визуально.

## Критерии хорошего ответа

### Что обязательно упомянуть

- comparisons
- AND/OR/NOT
- parentheses
- ranges

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- `status = 'paid' OR status = 'new' AND active` часто означает не ту группировку, которую читатель предполагает визуально.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с WHERE and boolean logic?

## Задача

Сделай короткую письменную практику по теме **WHERE and boolean logic**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `WHERE` фильтрует исходные rows по boolean predicates до grouping и aggregation.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** `status = 'paid' OR status = 'new' AND active` часто означает не ту группировку, которую читатель предполагает визуально.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
