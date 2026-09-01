# Primary and foreign keys

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Primary and foreign keys**, а не только запомнить термин;
- прочитать и изменить короткий пример для `entity identity`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**entity identity.** Identity отвечает на вопрос «тот же ли это объект» и сравнивается через `is`; равенство — отдельный протокол `__eq__`, обычно сравнивающий значения.

**referential целостность.** `referential integrity` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**delete/update actions.** `delete/update actions` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `entity identity` и `referential integrity` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `entity identity`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- entity identity
- referential целостность
- delete/update actions

### Полезно

- связать Primary and foreign keys с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Primary and foreign keys: отдельный пример

```sql
-- 11.1 · Primary and foreign keys
-- Focus: entity identity, referential integrity, delete/update actions
SELECT 's11_primary_and_foreign_keys' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Типичные ошибки

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `entity identity` до запуска.

**B · Найди ошибку.** Найди нарушение `referential integrity` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Primary and foreign keys за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Primary and foreign keys и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Primary and foreign keys: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный ответ уровня Junior

> Primary and foreign keys — тема, в которой я сначала фиксирую `entity identity`, затем объясняю `referential integrity` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Критерии хорошего ответа

### Что обязательно упомянуть

- entity identity
- referential целостность
- delete/update actions

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Primary and foreign keys?

## Задача

Сделай короткую письменную практику по теме **Primary and foreign keys**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Primary and foreign keys: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
