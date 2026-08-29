# Deadlocks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Deadlocks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `circular wait`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**circular wait.** `circular wait` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**consistent lock order.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**retry aborted transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `circular wait` и `consistent lock order` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `circular wait`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- circular wait
- consistent lock order
- retry aborted transaction

### Полезно

- связать Deadlocks с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Deadlocks: отдельный пример

```text
Сценарий: Два flow блокируют resources A/B в противоположном порядке.

Проверка:
Единый порядок lock acquisition, короткие transactions и retry всей transaction после deadlock.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `circular wait` до запуска.

**B · Find the bug.** Найди нарушение `consistent lock order` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Deadlocks за 60 секунд: определение, механизм, пример, ограничение.

## SQL practice

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

Seed:

```sql
INSERT INTO rooms VALUES (1,10,'101'),(2,10,'102');
INSERT INTO bookings VALUES
(1,1,'2026-09-01','2026-09-05','confirmed'),
(2,1,'2026-09-10','2026-09-12','cancelled');
```

**Вопрос:** Две transaction обновляют accounts A/B в разном порядке.

Expected columns: reasoning rubric. Comparison: reasoning_rubric.

SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric.

## Debugging practice

### Deadlock order

**Сценарий:** Два flow блокируют resources A/B в противоположном порядке.

**Rubric:** Единый порядок lock acquisition, короткие transactions и retry всей transaction после deadlock.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Deadlocks и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Deadlocks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Deadlocks: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный Junior answer

> Deadlocks — тема, в которой я сначала фиксирую `circular wait`, затем объясняю `consistent lock order` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Deadlocks?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Expected answer rubric

### Must mention

- circular wait
- consistent lock order
- retry aborted transaction

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Deadlocks?

## Задача

Сделай короткую письменную практику по теме **Deadlocks**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Deadlocks: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
