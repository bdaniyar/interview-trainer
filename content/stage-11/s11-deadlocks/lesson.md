# Deadlocks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Deadlocks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `circular wait`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**circular wait.** `circular wait` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**consistent lock order.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**retry aborted transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `circular wait` и `consistent lock order` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `circular wait`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- circular wait
- consistent lock order
- retry aborted transaction

### Полезно

- связать Deadlocks с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Deadlocks: отдельный пример

```text
Сценарий: Два flow блокируют resources A/B в противоположном порядке.

Проверка:
Единый порядок lock acquisition, короткие transactions и retry всей transaction после deadlock.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `circular wait` до запуска.

**B · Найди ошибку.** Найди нарушение `consistent lock order` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Deadlocks за 60 секунд: определение, механизм, пример, ограничение.

## Практика SQL

### Deadlock lock order

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

**Вопрос:** Две transaction обновляют accounts A/B в разном порядке.

Ожидаемые столбцы: критерии рассуждения. Сравнение: по критериям рассуждения.

Среда выполнения SQL пока не подключена: выполни запрос в локальном PostgreSQL и сверь результат с критериями.

## Практика: Отладка

### Deadlock order

**Сценарий:** Два flow блокируют resources A/B в противоположном порядке.

**Критерии ответа:** Единый порядок lock acquisition, короткие transactions и retry всей transaction после deadlock.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Deadlocks и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Deadlocks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Deadlocks: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный ответ уровня Junior

> Deadlocks — тема, в которой я сначала фиксирую `circular wait`, затем объясняю `consistent lock order` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Deadlocks?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Критерии хорошего ответа

### Что обязательно упомянуть

- circular wait
- consistent lock order
- retry aborted transaction

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Deadlocks?

## Задача

Сделай короткую письменную практику по теме **Deadlocks**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Deadlocks: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
