# Transactions and ACID

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Transactions and ACID**, а не только запомнить термин;
- прочитать и изменить короткий пример для `atomicity`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Transaction объединяет операции в одну атомарную границу; ACID означает atomicity, consistency, isolation и durability.

### Как работает

Commit фиксирует изменения, rollback отменяет их. Consistency обеспечивается правильным кодом и constraints, а не буквой C автоматически.


### Важный нюанс / ограничение

Transactions держат короткими и по возможности не выполняют внутри них сетевые вызовы, пока заняты locks и connection.

### Где используется в backend

Создание заказа и резервирование остатка должны входить в одну transaction, если этого требует invariant.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- atomicity
- consistency
- isolation
- durability

### Полезно

- transaction boundary

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Transactions and ACID: отдельный пример

```text
Сценарий: Request держит transaction открытой во время HTTP-вызова.

Проверка:
Сетевой I/O вынести за DB transaction; короткая boundary уменьшает locks, pool pressure и stale snapshot.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Commit внутри каждого repository call способен сохранить половину use case после ошибки следующего шага.

## Практика

**A · Предсказание результата.** Измени один input в примере `atomicity` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `consistency`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `atomicity`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Transactions and ACID за 45–60 секунд и назови одно ограничение.

## Практика SQL

### Atomic booking

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

**Вопрос:** Два запроса бронируют последний room одновременно. Где защитить инвариант?

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Long transaction

**Сценарий:** Request держит transaction открытой во время HTTP-вызова.

**Критерии ответа:** Сетевой I/O вынести за DB transaction; короткая boundary уменьшает locks, pool pressure и stale snapshot.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Double booking race

**Сценарий:** Два SELECT видят свободный номер и создают booking.

**Критерии ответа:** Защитить invariant в БД constraint/lock/conditional write и проверить concurrent integration test.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Transactions and ACID и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Transactions and ACID?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Transaction объединяет операции в одну атомарную границу; ACID означает atomicity, consistency, isolation и durability.

### Нормальный ответ уровня Junior

> Transaction объединяет операции в одну атомарную границу; ACID означает atomicity, consistency, isolation и durability. Commit фиксирует изменения, rollback отменяет их. Consistency обеспечивается правильным кодом и constraints, а не буквой C автоматически. Важное ограничение: Transactions держат короткими и по возможности не выполняют внутри них сетевые вызовы, пока заняты locks и connection.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Transactions and ACID?**

Commit внутри каждого repository call способен сохранить половину use case после ошибки следующего шага.

## Критерии хорошего ответа

### Что обязательно упомянуть

- atomicity
- consistency
- isolation
- durability

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Commit внутри каждого repository call способен сохранить половину use case после ошибки следующего шага.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Transactions and ACID?

## Задача

Сделай короткую письменную практику по теме **Transactions and ACID**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Transaction объединяет операции в одну атомарную границу; ACID означает atomicity, consistency, isolation и durability.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Commit внутри каждого repository call способен сохранить половину use case после ошибки следующего шага.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
