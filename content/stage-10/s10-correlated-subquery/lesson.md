# Correlated subquery

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Correlated subquery**, а не только запомнить термин;
- прочитать и изменить короткий пример для `per-row evaluation mental model`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Как работает

Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.

**per-row evaluation модель понимания.** `per-row evaluation mental model` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**optimizer caveat.** `optimizer caveat` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.

**alternatives.** `alternatives` меняет набор SQL rows; его смысл проверяют через grain результата, cardinality, NULL semantics и явный ordering.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `per-row evaluation mental model` и `optimizer caveat` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `per-row evaluation mental model`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- per-row evaluation модель понимания
- optimizer caveat
- alternatives

### Полезно

- связать Correlated subquery с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Correlated subquery: отдельный пример

```sql
SELECT p.id, p.title
FROM posts AS p
WHERE p.created_at = (
    SELECT MAX(inner_post.created_at)
    FROM posts AS inner_post
    WHERE inner_post.author_id = p.author_id
);
```

Correlated subquery ссылается на текущего outer author и выбирает его последний post.

## Типичные ошибки

### Ошибка 1

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `per-row evaluation mental model` до запуска.

**B · Найди ошибку.** Найди нарушение `optimizer caveat` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Correlated subquery за 60 секунд: определение, механизм, пример, ограничение.

## Практика SQL

### Последний заказ пользователя

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

**Вопрос:** Correlated subquery: верни orders, чей created_at максимален для своего user.

Ожидаемые столбцы: id, user_id. Сравнение: с учётом порядка строк.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое Correlated subquery и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Correlated subquery?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Correlated subquery: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.

### Нормальный ответ уровня Junior

> Correlated subquery — тема, в которой я сначала фиксирую `per-row evaluation mental model`, затем объясняю `optimizer caveat` на коротком примере. Ключевой механизм: Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа. Главная практическая ошибка — Не определить cardinality результата и замаскировать неверный query через DISTINCT.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Correlated subquery?**

Не определить cardinality результата и замаскировать неверный query через DISTINCT.

## Критерии хорошего ответа

### Что обязательно упомянуть

- per-row evaluation модель понимания
- optimizer caveat
- alternatives

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Correlated subquery?

## Задача

Сделай короткую письменную практику по теме **Correlated subquery**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Correlated subquery: Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.
- **Механизм:** Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.
- **Ограничение:** Не определить cardinality результата и замаскировать неверный query через DISTINCT.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL queries](https://www.postgresql.org/docs/current/queries.html)
- [PostgreSQL functions](https://www.postgresql.org/docs/current/functions.html)

Последняя проверка версий: **2026-08-27**.
