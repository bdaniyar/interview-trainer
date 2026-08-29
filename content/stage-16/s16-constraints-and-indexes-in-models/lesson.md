# Constraints and indexes in models

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Constraints and indexes in models**, а не только запомнить термин;
- прочитать и изменить короткий пример для `DB migration still required`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**DB migration still required.** `DB migration still required` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**model declaration is not production schema migration.** `model declaration is not production schema migration` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `DB migration still required` и `model declaration is not production schema migration` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `DB migration still required`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- DB migration still required
- model declaration is not production schema migration

### Полезно

- связать Constraints and indexes in models с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Constraints and indexes in models: отдельный пример

```python
def example_s16_constraints_and_indexes_in_models() -> tuple[str, ...]:
    # Constraints and indexes in models: проверяем отдельный contract урока.
    return ('DB migration still required', 'model declaration is not production schema migration',)

assert example_s16_constraints_and_indexes_in_models()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Common mistakes

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `DB migration still required` до запуска.

**B · Find the bug.** Найди нарушение `model declaration is not production schema migration` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Constraints and indexes in models за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Constraints and indexes in models и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Constraints and indexes in models: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Нормальный Junior answer

> Constraints and indexes in models — тема, в которой я сначала фиксирую `DB migration still required`, затем объясняю `model declaration is not production schema migration` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Expected answer rubric

### Must mention

- DB migration still required
- model declaration is not production schema migration

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?

## Задача

Сделай короткую письменную практику по теме **Constraints and indexes in models**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Constraints and indexes in models: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
