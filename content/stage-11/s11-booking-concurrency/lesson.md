# Booking concurrency

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Booking concurrency**, а не только запомнить термин;
- прочитать и изменить короткий пример для `check-then-insert race`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**check-then-insert race.** `check-then-insert race` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**unique/exclusion constraint.** Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

**conditional update.** `conditional update` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**row/advisory locks.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**`409 Conflict`.** ``409 Conflict`` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `check-then-insert race` и `unique/exclusion constraint` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `check-then-insert race`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- check-then-insert race
- unique/exclusion constraint
- conditional update
- row/advisory locks

### Полезно

- transaction
- `409 Conflict`

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Booking concurrency: отдельный пример

```sql
-- 11.17 · Booking concurrency
-- Focus: check-then-insert race, unique/exclusion constraint, conditional update, row/advisory locks
SELECT 's11_booking_concurrency' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `check-then-insert race` до запуска.

**B · Find the bug.** Найди нарушение `unique/exclusion constraint` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Booking concurrency за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Booking concurrency и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Booking concurrency?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Booking concurrency: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный Junior answer

> Booking concurrency — тема, в которой я сначала фиксирую `check-then-insert race`, затем объясняю `unique/exclusion constraint` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Booking concurrency?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Expected answer rubric

### Must mention

- check-then-insert race
- unique/exclusion constraint
- conditional update
- row/advisory locks

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Booking concurrency?

## Задача

Сделай короткую письменную практику по теме **Booking concurrency**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Booking concurrency: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
