# EXPLAIN and EXPLAIN ANALYZE

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **EXPLAIN and EXPLAIN ANALYZE**, а не только запомнить термин;
- прочитать и изменить короткий пример для `estimated vs actual`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`EXPLAIN` показывает план и estimates, а `EXPLAIN ANALYZE` действительно выполняет statement и добавляет actual rows и timing.

### Как работает

Plan читают от дочерних nodes вверх, сравнивая estimated и actual rows, loops, scan type и buffers.


### Важный нюанс / ограничение

ANALYZE реально выполняет изменяющий statement; такую проверку делают безопасно, например внутри transaction с rollback.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- estimated vs actual
- scan types
- rows
- loops

### Полезно

- timing
- ANALYZE executes the query

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### EXPLAIN and EXPLAIN ANALYZE: отдельный пример

```text
Сценарий: Planner выбирает Seq Scan для boolean active, хотя index существует.

Проверка:
При высокой доле совпадений Seq Scan может быть дешевле; сравнить estimates/actual rows, не принуждать index вслепую.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Просмотр только общего времени скрывает ошибку оценки rows или большое число loops, которое станет дорогим на реальных данных.

## Практика

**A · Предсказание результата.** Измени один input в примере `estimated vs actual` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `scan types`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `estimated vs actual`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни EXPLAIN and EXPLAIN ANALYZE за 45–60 секунд и назови одно ограничение.

## Практика SQL

### Sequential scan

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

**Вопрос:** После роста таблицы endpoint замедлился и plan показывает Seq Scan. План диагностики?

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Low-selectivity index

**Сценарий:** Planner выбирает Seq Scan для boolean active, хотя index существует.

**Критерии ответа:** При высокой доле совпадений Seq Scan может быть дешевле; сравнить estimates/actual rows, не принуждать index вслепую.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое EXPLAIN and EXPLAIN ANALYZE и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`EXPLAIN` показывает план и estimates, а `EXPLAIN ANALYZE` действительно выполняет statement и добавляет actual rows и timing.

### Нормальный ответ уровня Junior

> `EXPLAIN` показывает план и estimates, а `EXPLAIN ANALYZE` действительно выполняет statement и добавляет actual rows и timing. Plan читают от дочерних nodes вверх, сравнивая estimated и actual rows, loops, scan type и buffers. Важное ограничение: ANALYZE реально выполняет изменяющий statement; такую проверку делают безопасно, например внутри transaction с rollback.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?**

Просмотр только общего времени скрывает ошибку оценки rows или большое число loops, которое станет дорогим на реальных данных.

## Критерии хорошего ответа

### Что обязательно упомянуть

- estimated vs actual
- scan types
- rows
- loops

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Просмотр только общего времени скрывает ошибку оценки rows или большое число loops, которое станет дорогим на реальных данных.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с EXPLAIN and EXPLAIN ANALYZE?

## Задача

Сделай короткую письменную практику по теме **EXPLAIN and EXPLAIN ANALYZE**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `EXPLAIN` показывает план и estimates, а `EXPLAIN ANALYZE` действительно выполняет statement и добавляет actual rows и timing.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Просмотр только общего времени скрывает ошибку оценки rows или большое число loops, которое станет дорогим на реальных данных.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
