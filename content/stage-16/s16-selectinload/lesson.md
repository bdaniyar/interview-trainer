# `selectinload`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`selectinload`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `separate IN query`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**separate IN query.** `separate IN query` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**collections.** `collections` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**common safe default.** `common safe default` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `separate IN query` и `collections` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `separate IN query`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- separate IN query
- collections
- common safe default

### Полезно

- связать `selectinload` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `selectinload`: отдельный пример

```python
def projects_with_tasks(Project):
    raise NotImplementedError
```

Это публичный starter contract практики «selectinload collection». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `separate IN query` до запуска.

**B · Find the bug.** Найди нарушение `collections` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `selectinload` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `selectinload` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `selectinload`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`selectinload`: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Нормальный Junior answer

> `selectinload` — тема, в которой я сначала фиксирую `separate IN query`, затем объясняю `collections` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `selectinload`?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Expected answer rubric

### Must mention

- separate IN query
- collections
- common safe default

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `selectinload`?

## Задача

### selectinload collection

projects_with_tasks(Project): selectinload(Project.tasks), order id.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `selectinload`: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
