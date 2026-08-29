# Primary and foreign keys

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Primary and foreign keys**, а не только запомнить термин;
- прочитать и изменить короткий пример для `entity identity`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**entity identity.** Identity отвечает на вопрос «тот же ли это объект» и сравнивается через `is`; равенство — отдельный протокол `__eq__`, обычно сравнивающий значения.

**referential integrity.** `referential integrity` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**delete/update actions.** `delete/update actions` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `entity identity` и `referential integrity` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `entity identity`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- entity identity
- referential integrity
- delete/update actions

### Полезно

- связать Primary and foreign keys с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Primary and foreign keys: отдельный пример

```sql
-- 11.1 · Primary and foreign keys
-- Focus: entity identity, referential integrity, delete/update actions
SELECT 's11_primary_and_foreign_keys' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Common mistakes

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `entity identity` до запуска.

**B · Find the bug.** Найди нарушение `referential integrity` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Primary and foreign keys за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Primary and foreign keys и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Primary and foreign keys: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный Junior answer

> Primary and foreign keys — тема, в которой я сначала фиксирую `entity identity`, затем объясняю `referential integrity` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Expected answer rubric

### Must mention

- entity identity
- referential integrity
- delete/update actions

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?

## Задача

Сделай короткую письменную практику по теме **Primary and foreign keys**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Primary and foreign keys: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
