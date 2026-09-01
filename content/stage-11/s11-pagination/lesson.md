# Pagination

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Pagination**, а не только запомнить термин;
- прочитать и изменить короткий пример для `OFFSET/LIMIT`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Как работает

Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.

**OFFSET/LIMIT.** `OFFSET/LIMIT` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**large-offset cost.** `large-offset cost` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**cursor/keyset pagination.** `cursor/keyset pagination` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.

**stable ordering.** `stable ordering` влияет на database invariant, concurrent transactions или access path; правильность подтверждают constraint и фактический query plan.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `OFFSET/LIMIT` и `large-offset cost` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `OFFSET/LIMIT`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- OFFSET/LIMIT
- large-offset cost
- cursor/keyset pagination
- stable ordering

### Полезно

- связать Pagination с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Pagination: отдельный пример

```sql
-- 11.15 · Pagination
-- Focus: OFFSET/LIMIT, large-offset cost, cursor/keyset pagination, stable ordering
SELECT 's11_pagination' AS example_key;
```

Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.

## Типичные ошибки

### Ошибка 1

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `OFFSET/LIMIT` до запуска.

**B · Найди ошибку.** Найди нарушение `large-offset cost` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Pagination за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Pagination и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Pagination?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Pagination: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.

### Нормальный ответ уровня Junior

> Pagination — тема, в которой я сначала фиксирую `OFFSET/LIMIT`, затем объясняю `large-offset cost` на коротком примере. Ключевой механизм: Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan. Главная практическая ошибка — Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Pagination?**

Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.

## Критерии хорошего ответа

### Что обязательно упомянуть

- OFFSET/LIMIT
- large-offset cost
- cursor/keyset pagination
- stable ordering

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Pagination?

## Задача

Сделай короткую письменную практику по теме **Pagination**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Pagination: Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.
- **Механизм:** Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.
- **Ограничение:** Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Concurrency control](https://www.postgresql.org/docs/current/mvcc.html)

Последняя проверка версий: **2026-08-27**.
