# Authentication and permissions

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Authentication and permissions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `global vs per-view`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Authentication and permissions** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**global vs per-view.** `global vs per-view` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.

**object-level permission.** `object-level permission` входит в Django/DRF request flow и влияет на ORM query count, validation, permissions или response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `global vs per-view` и `object-level permission` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `global vs per-view`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- global vs per-view
- object-level permission

### Полезно

- связать Authentication and permissions с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Authentication and permissions: отдельный пример

```python
def example_s26_authentication_and_permissions() -> tuple[str, ...]:
    # Authentication and permissions: проверяем отдельный contract урока.
    return ('global vs per-view', 'object-level permission',)

assert example_s26_authentication_and_permissions()
```

Проследи Django/DRF request, ORM query count, validation, permission и response.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `global vs per-view` до запуска.

**B · Find the bug.** Найди нарушение `object-level permission` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Authentication and permissions за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Authentication and permissions и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Authentication and permissions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Authentication and permissions: это отдельный технический контракт

### Нормальный Junior answer

> Authentication and permissions — тема, в которой я сначала фиксирую `global vs per-view`, затем объясняю `object-level permission` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Authentication and permissions?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- global vs per-view
- object-level permission

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Authentication and permissions?

## Задача

Сделай короткую письменную практику по теме **Authentication and permissions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Authentication and permissions: это отдельный технический контракт
- **Механизм:** Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
