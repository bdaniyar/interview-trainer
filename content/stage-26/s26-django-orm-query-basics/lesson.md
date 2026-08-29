# Django ORM query basics

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Django ORM query basics**, а не только запомнить термин;
- прочитать и изменить короткий пример для `filter`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Django ORM query basics** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**filter.** `filter` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**get.** `get` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**create.** `create` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**update.** `update` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**delete.** `delete` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**lazy QuerySet.** `lazy QuerySet` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `filter` и `get` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `filter`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- filter
- get
- create
- update

### Полезно

- delete
- lazy QuerySet

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Django ORM query basics: отдельный пример

```python
def example_s26_django_orm_query_basics() -> tuple[str, ...]:
    # Django ORM query basics: проверяем отдельный contract урока.
    return ('filter', 'get', 'create', 'update',)

assert example_s26_django_orm_query_basics()
```

Проследи Django/DRF request, ORM query count, validation, permission и response.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `filter` до запуска.

**B · Find the bug.** Найди нарушение `get` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Django ORM query basics за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Django ORM query basics и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Django ORM query basics?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Django ORM query basics: это отдельный технический контракт

### Нормальный Junior answer

> Django ORM query basics — тема, в которой я сначала фиксирую `filter`, затем объясняю `get` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Django ORM query basics?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- filter
- get
- create
- update

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Django ORM query basics?

## Задача

Сделай короткую письменную практику по теме **Django ORM query basics**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Django ORM query basics: это отдельный технический контракт
- **Механизм:** Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
