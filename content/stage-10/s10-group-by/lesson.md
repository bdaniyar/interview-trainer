# GROUP BY

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **GROUP BY**, а не только запомнить термин;
- прочитать и изменить короткий пример для `grouping`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`GROUP BY` формирует группы rows и возвращает одну result row для каждого уникального grouping key.

### Как работает

Aggregate functions считают значения внутри группы. Выбранные неагрегированные columns обычно должны находиться в GROUP BY.


### Важный нюанс / ограничение

Сначала назови grain результата, например «одна строка на `user_id`», и только потом добавляй joins, способные размножить source rows.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- grouping
- selected non-aggregate columns
- common errors

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### GROUP BY: отдельный пример

```sql
SELECT customer_id, SUM(total) AS revenue
FROM invoices
WHERE paid_at IS NOT NULL
GROUP BY customer_id
ORDER BY customer_id;
```

GROUP BY задаёт grain «одна строка на customer», после чего SUM считает значение внутри каждой группы.

## Типичные ошибки

### Ошибка 1

Grouping после one-to-many join может посчитать сумму дважды, если grain join мельче измеряемого показателя.

## Практика

**A · Предсказание результата.** Измени один input в примере `grouping` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `selected non-aggregate columns`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `grouping`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни GROUP BY за 45–60 секунд и назови одно ограничение.

## Практика SQL

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

**Вопрос:** Посчитай заказы по status и отсортируй status.

Ожидаемые столбцы: status, count. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

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

**Вопрос:** Суммируй total только paid-заказов по user_id.

Ожидаемые столбцы: user_id, revenue. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

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

**Вопрос:** Найди средний total paid-заказа.

Ожидаемые столбцы: average_total. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### COUNT nullable

**Сценарий:** COUNT(country) меньше COUNT(*).

**Критерии ответа:** COUNT(expression) пропускает NULL.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Incorrect GROUP BY

**Сценарий:** Запрос агрегирует по user_id, но выбирает произвольный email.

**Критерии ответа:** Все неагрегированные columns должны быть функционально зависимы/в GROUP BY; сначала определить grain результата.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое GROUP BY и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с GROUP BY?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`GROUP BY` формирует группы rows и возвращает одну result row для каждого уникального grouping key.

### Нормальный ответ уровня Junior

> `GROUP BY` формирует группы rows и возвращает одну result row для каждого уникального grouping key. Aggregate functions считают значения внутри группы. Выбранные неагрегированные columns обычно должны находиться в GROUP BY. Важное ограничение: Сначала назови grain результата, например «одна строка на `user_id`», и только потом добавляй joins, способные размножить source rows.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с GROUP BY?**

Grouping после one-to-many join может посчитать сумму дважды, если grain join мельче измеряемого показателя.

## Критерии хорошего ответа

### Что обязательно упомянуть

- grouping
- selected non-aggregate columns
- common errors

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Grouping после one-to-many join может посчитать сумму дважды, если grain join мельче измеряемого показателя.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с GROUP BY?

## Задача

Сделай короткую письменную практику по теме **GROUP BY**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `GROUP BY` формирует группы rows и возвращает одну result row для каждого уникального grouping key.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Grouping после one-to-many join может посчитать сумму дважды, если grain join мельче измеряемого показателя.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
