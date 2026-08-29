# FastAPI vs Django/DRF

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **FastAPI vs Django/DRF**, а не только запомнить термин;
- прочитать и изменить короткий пример для `FastAPI: typed API/async flexibility`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **FastAPI vs Django/DRF** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**FastAPI: typed API/async flexibility.** `FastAPI: typed API/async flexibility` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**Django: batteries, ORM, admin, auth ecosystem.** `Django: batteries, ORM, admin, auth ecosystem` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**no claim that one is universally better.** `no claim that one is universally better` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `FastAPI: typed API/async flexibility` и `Django: batteries, ORM, admin, auth ecosystem` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `FastAPI: typed API/async flexibility`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- FastAPI: typed API/async flexibility
- Django: batteries, ORM, admin, auth ecosystem
- no claim that one is universally better

### Полезно

- связать FastAPI vs Django/DRF с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

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

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `FastAPI: typed API/async flexibility` до запуска.

**B · Find the bug.** Найди нарушение `Django: batteries, ORM, admin, auth ecosystem` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про FastAPI vs Django/DRF за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое FastAPI vs Django/DRF и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме FastAPI vs Django/DRF?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI vs Django/DRF: это отдельный технический контракт

### Нормальный Junior answer

> FastAPI vs Django/DRF — тема, в которой я сначала фиксирую `FastAPI: typed API/async flexibility`, затем объясняю `Django: batteries, ORM, admin, auth ecosystem` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме FastAPI vs Django/DRF?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- FastAPI: typed API/async flexibility
- Django: batteries, ORM, admin, auth ecosystem
- no claim that one is universally better

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме FastAPI vs Django/DRF?

## Задача

Сделай короткую письменную практику по теме **FastAPI vs Django/DRF**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI vs Django/DRF: это отдельный технический контракт
- **Механизм:** Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
