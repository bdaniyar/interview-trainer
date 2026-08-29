# EXISTS vs IN

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **EXISTS vs IN**, а не только запомнить термин;
- прочитать и изменить короткий пример для `existence semantics`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Как работает

Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.

**existence semantics.** `existence semantics` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**NULL caveats.** `NULL` означает отсутствие известного значения; сравнение с ним делают через `IS NULL`, а многие выражения дают `UNKNOWN`.

**no simplistic universal performance rule.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `existence semantics` и `NULL caveats` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `existence semantics`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- existence semantics
- NULL caveats
- no simplistic universal performance rule

### Полезно

- связать EXISTS vs IN с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### EXISTS vs IN: отдельный пример

```sql
SELECT u.id
FROM users AS u
WHERE EXISTS (
    SELECT 1 FROM sessions AS s
    WHERE s.user_id = u.id AND s.revoked_at IS NULL
);
```

EXISTS выражает проверку наличия связанной строки и не размножает users как обычный JOIN.

## Common mistakes

### Ошибка 1

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `existence semantics` до запуска.

**B · Find the bug.** Найди нарушение `NULL caveats` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про EXISTS vs IN за 60 секунд: определение, механизм, пример, ограничение.

## SQL practice

### Users с paid order

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

**Вопрос:** Через EXISTS верни users, у которых есть paid order.

Expected columns: id, email. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

### Users без orders

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

**Вопрос:** Через NOT EXISTS верни users без orders.

Expected columns: id. Comparison: unordered.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Interview questions

### Основной вопрос

Что такое EXISTS vs IN и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме EXISTS vs IN?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

EXISTS vs IN: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Нормальный Junior answer

> EXISTS vs IN — тема, в которой я сначала фиксирую `existence semantics`, затем объясняю `NULL caveats` на коротком примере. Ключевой механизм: Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа. Главная практическая ошибка — Не определить cardinality результата и замаскировать неверный query через DISTINCT.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме EXISTS vs IN?**

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Expected answer rubric

### Must mention

- existence semantics
- NULL caveats
- no simplistic universal performance rule

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме EXISTS vs IN?

## Задача

Сделай короткую письменную практику по теме **EXISTS vs IN**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** EXISTS vs IN: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
