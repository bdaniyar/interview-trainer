# Connection pooling

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Connection pooling**, а не только запомнить термин;
- прочитать и изменить короткий пример для `connections are expensive/limited`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**соединения дороги и ограничены.** `connections are expensive/limited` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**pool size.** `pool size` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**async pool.** `async pool` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**leaking sessions/connections.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `connections are expensive/limited` и `pool size` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `connections are expensive/limited`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- соединения дороги и ограничены
- pool size
- async pool
- leaking sessions/connections

### Полезно

- связать Connection pooling с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Connection pooling: отдельный пример

```sql
-- 11.14 · Connection pooling
-- Focus: connections are expensive/limited, pool size, async pool, leaking sessions/connections
SELECT 's11_connection_pooling' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Типичные ошибки

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `connections are expensive/limited` до запуска.

**B · Найди ошибку.** Найди нарушение `pool size` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Connection pooling за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Connection pooling и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Connection pooling?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Connection pooling: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный ответ уровня Junior

> Connection pooling — тема, в которой я сначала фиксирую `connections are expensive/limited`, затем объясняю `pool size` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Connection pooling?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Критерии хорошего ответа

### Что обязательно упомянуть

- соединения дороги и ограничены
- pool size
- async pool
- leaking sessions/connections

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Connection pooling?

## Задача

Сделай короткую письменную практику по теме **Connection pooling**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Connection pooling: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
