# Index mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Index mental model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `auxiliary data structure`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Database index — вспомогательная структура, позволяющая находить упорядоченные ranges ключей без полного table scan.

### Как работает

Index ускоряет подходящий access path, но занимает место и добавляет работу INSERT/UPDATE/DELETE. Planner может выбрать sequential scan, когда совпадает большая часть rows.


### Важный нюанс / ограничение

Проектируй indexes по реальным WHERE/JOIN/ORDER patterns и проверяй `EXPLAIN ANALYZE`; index на каждую column вреден.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Index mental model: отдельный пример

```text
Сценарий: Lookup по уникальному external_id замедлился после роста таблицы.

Проверка:
Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Index без конкретного query shape и selectivity увеличивает стоимость writes и может никогда не использоваться.

## Практика

**A · Предсказание результата.** Измени один input в примере `auxiliary data structure` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `faster reads`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `auxiliary data structure`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Index модель понимания за 45–60 секунд и назови одно ограничение.

## Практика SQL

### Index для email lookup

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

**Вопрос:** GET /users/by-email выполняет WHERE lower(email)=lower($1), но индекс только на email. Что проверить?

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Missing index

**Сценарий:** Lookup по уникальному external_id замедлился после роста таблицы.

**Критерии ответа:** Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Index модель понимания и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Index модель понимания?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Database index — вспомогательная структура, позволяющая находить упорядоченные ranges ключей без полного table scan.

### Нормальный ответ уровня Junior

> Database index — вспомогательная структура, позволяющая находить упорядоченные ranges ключей без полного table scan. Index ускоряет подходящий access path, но занимает место и добавляет работу INSERT/UPDATE/DELETE. Planner может выбрать sequential scan, когда совпадает большая часть rows. Важное ограничение: Проектируй indexes по реальным WHERE/JOIN/ORDER patterns и проверяй `EXPLAIN ANALYZE`; index на каждую column вреден.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Index модель понимания?**

Index без конкретного query shape и selectivity увеличивает стоимость writes и может никогда не использоваться.

## Критерии хорошего ответа

### Что обязательно упомянуть

- auxiliary data structure
- faster reads
- storage/write cost
- index is not magic

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Index без конкретного query shape и selectivity увеличивает стоимость writes и может никогда не использоваться.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Index модель понимания?

## Задача

Сделай короткую письменную практику по теме **Index mental model**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Database index — вспомогательная структура, позволяющая находить упорядоченные ranges ключей без полного table scan.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Index без конкретного query shape и selectivity увеличивает стоимость writes и может никогда не использоваться.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
