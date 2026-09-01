# CTE

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **CTE**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``WITH``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

CTE (common table expression) — именованный промежуточный result, объявленный через `WITH` и доступный основному statement. Он помогает разбить длинный SQL на последовательные понятные шаги.

### Как работает

Каждый CTE имеет имя и query в скобках. Следующий CTE или основной SELECT обращается к нему как к таблице. Обычный CTE живёт только во время одного statement; recursive CTE может ссылаться на себя по специальным правилам.


### Пример

```sql
WITH paid_totals AS (
    SELECT user_id, SUM(total) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT user_id, revenue
FROM paid_totals
WHERE revenue >= 100;
```

Сначала `paid_totals` даёт одну строку на user, затем внешний query фильтрует уже рассчитанный revenue.

### Важный нюанс / ограничение

CTE — прежде всего средство выразительности, не гарантированная оптимизация. Современный PostgreSQL может встроить не recursive CTE в plan; `MATERIALIZED`/`NOT MATERIALIZED` влияют на это. Junior достаточно читать EXPLAIN, а не обещать ускорение.

### Где используется в backend

CTE удобно отделяет выбор paid orders, aggregation по пользователю и финальный фильтр отчёта в одном statement.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- синтаксис WITH
- scope одного statement
- читаемые этапы
- нет гарантии ускорения

### Полезно

- multiple CTE
- recursive CTE на уровне идеи
- planner/materialization caveat

### Можно не учить глубоко

- тонкости cost model materialization без EXPLAIN конкретного запроса

## Примеры кода

### CTE: отдельный пример

```sql
WITH monthly AS (
    SELECT date_trunc('month', created_at) AS month, SUM(total) AS revenue
    FROM invoices
    GROUP BY date_trunc('month', created_at)
)
SELECT month, revenue
FROM monthly
WHERE revenue > 1000;
```

CTE именует промежуточный result и отделяет aggregation от последующей фильтрации.

## Типичные ошибки

### Ошибка 1

Считать, что `WITH` автоматически ускоряет запрос.

### Ошибка 2

Спрятать неверную cardinality в цепочке CTE и не проверять результат каждого шага.

### Ошибка 3

Использовать CTE из одного простого SELECT, когда он только увеличивает объём кода.

## Практика

**A · Result предсказание результата.** Назови grain каждого шага monthly и итогового SELECT.

**B · Найди ошибку.** Найди фильтр, применённый до нужной aggregation.

**C · Улучшение кода.** Разбей вложенный отчёт на два именованных CTE.

**D · SQL task.** Найди users с paid revenue выше порога.

## Практика SQL

### CTE revenue

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

**Вопрос:** CTE paid_totals считает paid revenue по user, затем оставь revenue >= 150.

Ожидаемые столбцы: user_id, revenue. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

### Цепочка менеджеров

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

**Вопрос:** Recursive CTE от user 4 вверх по manager_id, верни id и depth.

Ожидаемые столбцы: id, depth. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое CTE и гарантирует ли он ускорение SQL-запроса?

### Дополнительный вопрос

Чем CTE отличается от view?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

CTE — именованный промежуточный query через WITH; он улучшает структуру, но сам по себе не гарантирует производительность.

### Нормальный ответ уровня Junior

> CTE объявляется через `WITH name AS (...)` и доступен последующему query как временный result. Я использую его, чтобы дать имя этапу — например, сначала посчитать revenue по месяцу, затем отфильтровать итог. Это не обещание ускорения: PostgreSQL может встроить или материализовать CTE, поэтому производительность проверяют через EXPLAIN.

### Углубление / дополнительный вопрос

**Чем CTE отличается от view?**

CTE существует только в одном statement; view — сохранённое определение query в schema и может использоваться разными statements.

## Критерии хорошего ответа

### Что обязательно упомянуть

- синтаксис WITH
- scope одного statement
- читаемые этапы
- нет гарантии ускорения

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Считать, что `WITH` автоматически ускоряет запрос.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Чем CTE отличается от view?

## Задача

Сделай короткую письменную практику по теме **CTE**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** CTE — именованный промежуточный query через WITH; он улучшает структуру, но сам по себе не гарантирует производительность.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Считать, что `WITH` автоматически ускоряет запрос.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
