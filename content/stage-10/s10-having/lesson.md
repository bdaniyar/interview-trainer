# HAVING

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **HAVING**, а не только запомнить термин;
- прочитать и изменить короткий пример для `WHERE before grouping`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`HAVING` фильтрует группы после aggregation, а `WHERE` отбирает исходные rows до формирования групп.

### Как работает

Условие на обычные rows относится к WHERE; условие вроде `COUNT(*) >= 2` — к HAVING.


### Важный нюанс / ограничение

Перенос фильтра через границу aggregation способен изменить и состав групп, и набор surviving groups.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- WHERE before grouping
- HAVING after grouping
- реалистичные примеры заказов и клиентов

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### HAVING: отдельный пример

```sql
SELECT author_id, COUNT(*) AS article_count
FROM articles
GROUP BY author_id
HAVING COUNT(*) >= 3;
```

HAVING фильтрует уже сформированные группы; аналогичный predicate нельзя применить в WHERE до aggregation.

## Типичные ошибки

### Ошибка 1

`WHERE COUNT(*) > 1` некорректен, потому что aggregate на этом этапе ещё не вычислен.

## Практика

**A · Предсказание результата.** Измени один input в примере `WHERE before grouping` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `HAVING after grouping`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `WHERE before grouping`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни HAVING за 45–60 секунд и назови одно ограничение.

## Практика SQL

### Пользователи с двумя заказами

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

**Вопрос:** Верни user_id с минимум двумя заказами.

Ожидаемые столбцы: user_id, count. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое HAVING и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с HAVING?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`HAVING` фильтрует группы после aggregation, а `WHERE` отбирает исходные rows до формирования групп.

### Нормальный ответ уровня Junior

> `HAVING` фильтрует группы после aggregation, а `WHERE` отбирает исходные rows до формирования групп. Условие на обычные rows относится к WHERE; условие вроде `COUNT(*) >= 2` — к HAVING. Важное ограничение: Перенос фильтра через границу aggregation способен изменить и состав групп, и набор surviving groups.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с HAVING?**

`WHERE COUNT(*) > 1` некорректен, потому что aggregate на этом этапе ещё не вычислен.

## Критерии хорошего ответа

### Что обязательно упомянуть

- WHERE before grouping
- HAVING after grouping
- реалистичные примеры заказов и клиентов

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- `WHERE COUNT(*) > 1` некорректен, потому что aggregate на этом этапе ещё не вычислен.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с HAVING?

## Задача

Сделай короткую письменную практику по теме **HAVING**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `HAVING` фильтрует группы после aggregation, а `WHERE` отбирает исходные rows до формирования групп.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** `WHERE COUNT(*) > 1` некорректен, потому что aggregate на этом этапе ещё не вычислен.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
