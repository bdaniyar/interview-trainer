# FastAPI vs Django/DRF

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- объяснить `FastAPI: typed API/async flexibility` своими словами и связать с backend-сценарием;
- объяснить `Django: batteries, ORM, admin, auth ecosystem` своими словами и связать с backend-сценарием;
- объяснить `no claim that one is universally better.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Django/DRF предоставляет batteries-included стек: ORM, migrations, admin, auth и API abstractions.

В теме **FastAPI vs Django/DRF** важно уверенно объяснять следующие части:

### FastAPI: typed API/async flexibility

Для `FastAPI: typed API/async flexibility` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.

### Django: batteries, ORM, admin, auth ecosystem

Для `Django: batteries, ORM, admin, auth ecosystem` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.

### no claim that one is universally better

Для `no claim that one is universally better` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### FastAPI vs Django/DRF: отдельный пример

```python
def example_s26_fastapi_vs_django_drf() -> tuple[str, ...]:
    # FastAPI vs Django/DRF: проверяем отдельный contract урока.
    return ('FastAPI: typed API/async flexibility', 'Django: batteries, ORM, admin, auth ecosystem', 'no claim that one is universally better',)

assert example_s26_fastapi_vs_django_drf()
```

Проследи Django/DRF request, ORM query count, validation, permission и response.

## Common mistakes

**Ошибка:** Путать select_related и prefetch_related или переносить FastAPI patterns дословно.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **FastAPI vs Django/DRF** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни request flow и data access одного endpoint в DRF и FastAPI. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- FastAPI: typed API/async flexibility
- Django: batteries, ORM, admin, auth ecosystem
- no claim that one is universally better.
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

- FastAPI: typed API/async flexibility
- Django: batteries, ORM, admin, auth ecosystem
- no claim that one is universally better.

## Задача

Разбери backend-сценарий: **Сравни request flow и data access одного endpoint в DRF и FastAPI.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **FastAPI vs Django/DRF**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
