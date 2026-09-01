# Composite indexes and column order

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Composite indexes and column order**, а не только запомнить термин;
- прочитать и изменить короткий пример для `leftmost prefix intuition`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**leftmost prefix intuition.** Router prefix добавляется ко всем путям группы и позволяет собирать модульный API без повторения `/users` или `/v1` в каждом decorator.

**filter/order patterns.** `filter/order patterns` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**равенство перед диапазоном — практическая эвристика, а не догма.** `equality before range as a heuristic, not dogma` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `leftmost prefix intuition` и `filter/order patterns` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `leftmost prefix intuition`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- leftmost prefix intuition
- filter/order patterns
- равенство перед диапазоном — практическая эвристика, а не догма

### Полезно

- связать Composite indexes and column order с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Composite indexes and column order: отдельный пример

```sql
-- 11.6 · Composite indexes and column order
-- Focus: leftmost prefix intuition, filter/order patterns, equality before range as a heuristic, not dogma
SELECT 's11_composite_indexes_and_column_order' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Типичные ошибки

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `leftmost prefix intuition` до запуска.

**B · Найди ошибку.** Найди нарушение `filter/order patterns` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Composite indexes and column order за 60 секунд: определение, механизм, пример, ограничение.

## Практика SQL

### Composite index order

```sql
CREATE TABLE rooms (
    id bigint PRIMARY KEY,
    hotel_id bigint NOT NULL,
    number text NOT NULL,
    UNIQUE (hotel_id, number)
);
CREATE TABLE bookings (
    id bigint PRIMARY KEY,
    room_id bigint NOT NULL REFERENCES rooms(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL,
    CHECK (ends_at > starts_at)
);
```

Начальные данные:

```sql
INSERT INTO rooms VALUES (1,10,'101'),(2,10,'102');
INSERT INTO bookings VALUES
(1,1,'2026-09-01','2026-09-05','confirmed'),
(2,1,'2026-09-10','2026-09-12','cancelled');
```

**Вопрос:** Запрос WHERE hotel_id=$1 AND starts_at >= $2 ORDER BY starts_at. Предложи индекс.

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое Composite indexes and column order и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Composite indexes and column order?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Composite indexes and column order: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный ответ уровня Junior

> Composite indexes and column order — тема, в которой я сначала фиксирую `leftmost prefix intuition`, затем объясняю `filter/order patterns` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Composite indexes and column order?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Критерии хорошего ответа

### Что обязательно упомянуть

- leftmost prefix intuition
- filter/order patterns
- равенство перед диапазоном — практическая эвристика, а не догма

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Composite indexes and column order?

## Задача

Сделай короткую письменную практику по теме **Composite indexes and column order**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Composite indexes and column order: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
