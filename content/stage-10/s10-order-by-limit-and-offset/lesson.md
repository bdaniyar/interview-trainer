# ORDER BY, LIMIT and OFFSET

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **ORDER BY, LIMIT and OFFSET**, а не только запомнить термин;
- прочитать и изменить короткий пример для `deterministic ordering`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`ORDER BY` задаёт порядок результата, `LIMIT` ограничивает rows, а `OFFSET` пропускает строки для простой pagination.

### Как работает

Несколько полей сортировки применяются слева направо. Уникальный tie-breaker вроде id нужен для детерминированных страниц при одинаковом основном значении.


### Важный нюанс / ограничение

Большой OFFSET заставляет БД просмотреть и отбросить предыдущие rows, а concurrent inserts сдвигают границы страниц; keyset pagination масштабируется лучше.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- deterministic ordering
- multi-column ordering
- pagination caveats

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### ORDER BY, LIMIT and OFFSET: отдельный пример

```sql
SELECT id, created_at
FROM events
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 20;
```

Уникальный `id` — tie-breaker: страницы остаются детерминированными при одинаковом времени.

## Типичные ошибки

### Ошибка 1

LIMIT/OFFSET без стабильного уникального ordering возвращает пропущенные или повторные rows между страницами.

## Практика

**A · Предсказание результата.** Измени один input в примере `deterministic ordering` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `multi-column ordering`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `deterministic ordering`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни ORDER BY, LIMIT and OFFSET за 45–60 секунд и назови одно ограничение.

## Практика SQL

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

**Вопрос:** Верни два последних заказа по created_at, при равенстве — больший id первым.

Ожидаемые столбцы: id, created_at. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

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

**Вопрос:** Верни вторую страницу пользователей размера 2 с устойчивым order по id.

Ожидаемые столбцы: id, email. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Missing deterministic order

**Сценарий:** LIMIT 20 иногда возвращает другой набор строк.

**Критерии ответа:** Добавить ORDER BY с уникальным tie-breaker; без него SQL не обещает порядок.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое ORDER BY, LIMIT and OFFSET и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`ORDER BY` задаёт порядок результата, `LIMIT` ограничивает rows, а `OFFSET` пропускает строки для простой pagination.

### Нормальный ответ уровня Junior

> `ORDER BY` задаёт порядок результата, `LIMIT` ограничивает rows, а `OFFSET` пропускает строки для простой pagination. Несколько полей сортировки применяются слева направо. Уникальный tie-breaker вроде id нужен для детерминированных страниц при одинаковом основном значении. Важное ограничение: Большой OFFSET заставляет БД просмотреть и отбросить предыдущие rows, а concurrent inserts сдвигают границы страниц; keyset pagination масштабируется лучше.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?**

LIMIT/OFFSET без стабильного уникального ordering возвращает пропущенные или повторные rows между страницами.

## Критерии хорошего ответа

### Что обязательно упомянуть

- deterministic ordering
- multi-column ordering
- pagination caveats

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- LIMIT/OFFSET без стабильного уникального ordering возвращает пропущенные или повторные rows между страницами.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с ORDER BY, LIMIT and OFFSET?

## Задача

Сделай короткую письменную практику по теме **ORDER BY, LIMIT and OFFSET**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `ORDER BY` задаёт порядок результата, `LIMIT` ограничивает rows, а `OFFSET` пропускает строки для простой pagination.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** LIMIT/OFFSET без стабильного уникального ordering возвращает пропущенные или повторные rows между страницами.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
