# Window functions

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Window functions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `rows remain visible`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Window function вычисляет значение по связанным rows, сохраняя каждую исходную row, в отличие от GROUP BY.

### Как работает

`OVER` задаёт partition, order и frame. Типичные случаи — ranking, running total и сравнение с предыдущей row.


### Важный нюанс / ограничение

Ordering внутри OVER управляет window calculation; финальный порядок результата всё равно требует отдельного ORDER BY.

### Где используется в backend

Report может добавить накопительную сумму по customer, не теряя отдельные transactions.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- rows remain visible
- difference from GROUP BY
- window definition

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Отсутствие tie-breaker в window ordering делает `row_number` недетерминированным при равных значениях.

## Практика

**A · Предсказание результата.** Измени один input в примере `rows remain visible` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `difference from GROUP BY`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `rows remain visible`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Window functions за 45–60 секунд и назови одно ограничение.

## Практика SQL

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

**Вопрос:** Добавь previous_total через LAG в рамках user.

Ожидаемые столбцы: id, user_id, total, previous_total. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

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

**Вопрос:** Добавь next_created_at через LEAD в рамках user.

Ожидаемые столбцы: id, user_id, next_created_at. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое Window functions и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Window functions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Window function вычисляет значение по связанным rows, сохраняя каждую исходную row, в отличие от GROUP BY.

### Нормальный ответ уровня Junior

> Window function вычисляет значение по связанным rows, сохраняя каждую исходную row, в отличие от GROUP BY. `OVER` задаёт partition, order и frame. Типичные случаи — ranking, running total и сравнение с предыдущей row. Важное ограничение: Ordering внутри OVER управляет window calculation; финальный порядок результата всё равно требует отдельного ORDER BY.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Window functions?**

Отсутствие tie-breaker в window ordering делает `row_number` недетерминированным при равных значениях.

## Критерии хорошего ответа

### Что обязательно упомянуть

- rows remain visible
- difference from GROUP BY
- window definition

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Отсутствие tie-breaker в window ordering делает `row_number` недетерминированным при равных значениях.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Window functions?

## Задача

Сделай короткую письменную практику по теме **Window functions**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Window function вычисляет значение по связанным rows, сохраняя каждую исходную row, в отличие от GROUP BY.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Отсутствие tie-breaker в window ordering делает `row_number` недетерминированным при равных значениях.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
