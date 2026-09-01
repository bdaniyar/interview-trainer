# Isolation levels

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Isolation levels**, а не только запомнить термин;
- прочитать и изменить короткий пример для `read committed`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Isolation levels определяют, какие эффекты concurrent transactions могут наблюдать друг у друга.

### Как работает

PostgreSQL Read Committed использует snapshot на statement, Repeatable Read сохраняет snapshot transaction, а Serializable может отменить transaction ради последовательной семантики.


### Важный нюанс / ограничение

Более строгая isolation не бесплатна, а serialization failure требует retry всей transaction.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- read committed
- repeatable read
- serializable
- anomalies at reasonable depth

### Полезно

- PostgreSQL-specific behavior

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Isolation levels: отдельный пример

```sql
-- 11.10 · Isolation levels
-- Focus: read committed, repeatable read, serializable, anomalies at reasonable depth
SELECT 's11_isolation_levels' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Типичные ошибки

### Ошибка 1

Повышение isolation без названной anomaly увеличивает contention и может не защитить реальный invariant.

## Практика

**A · Предсказание результата.** Измени один input в примере `read committed` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `repeatable read`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `read committed`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Isolation levels за 45–60 секунд и назови одно ограничение.

## Практика SQL

### Isolation anomaly

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

**Вопрос:** Две transaction читают доступный balance и обе списывают средства. Что гарантирует Read Committed?

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Вопросы с собеседований

### Основной вопрос

Что такое Isolation levels и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Isolation levels?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Isolation levels определяют, какие эффекты concurrent transactions могут наблюдать друг у друга.

### Нормальный ответ уровня Junior

> Isolation levels определяют, какие эффекты concurrent transactions могут наблюдать друг у друга. PostgreSQL Read Committed использует snapshot на statement, Repeatable Read сохраняет snapshot transaction, а Serializable может отменить transaction ради последовательной семантики. Важное ограничение: Более строгая isolation не бесплатна, а serialization failure требует retry всей transaction.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Isolation levels?**

Повышение isolation без названной anomaly увеличивает contention и может не защитить реальный invariant.

## Критерии хорошего ответа

### Что обязательно упомянуть

- read committed
- repeatable read
- serializable
- anomalies at reasonable depth

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Повышение isolation без названной anomaly увеличивает contention и может не защитить реальный invariant.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Isolation levels?

## Задача

Сделай короткую письменную практику по теме **Isolation levels**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Isolation levels определяют, какие эффекты concurrent transactions могут наблюдать друг у друга.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Повышение isolation без названной anomaly увеличивает contention и может не защитить реальный invariant.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
