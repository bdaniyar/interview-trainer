# DRF testing

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- объяснить `DRF testing` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Django/DRF предоставляет batteries-included стек: ORM, migrations, admin, auth и API abstractions.

В теме **DRF testing** важно уверенно объяснять следующие части:

### DRF testing

Для `DRF testing` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### DRF testing: отдельный пример

```python
def example_s26_drf_testing() -> tuple[str, ...]:
    # DRF testing: проверяем отдельный contract урока.
    return ('DRF testing',)

assert example_s26_drf_testing()
```

Проследи Django/DRF request, ORM query count, validation, permission и response.

## Common mistakes

**Ошибка:** Путать select_related и prefetch_related или переносить FastAPI patterns дословно.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **DRF testing** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни request flow и data access одного endpoint в DRF и FastAPI. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- DRF testing
- Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Путать select_related и prefetch_related или переносить FastAPI patterns дословно.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- DRF testing

## Задача

Разбери backend-сценарий: **Сравни request flow и data access одного endpoint в DRF и FastAPI.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **DRF testing**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
