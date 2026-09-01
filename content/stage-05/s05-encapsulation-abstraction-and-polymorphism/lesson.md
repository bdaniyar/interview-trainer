# Encapsulation, abstraction and polymorphism

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Encapsulation, abstraction and polymorphism**, а не только запомнить термин;
- прочитать и изменить короткий пример для `practical Python meaning`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Encapsulation объединяет состояние и поведение, abstraction показывает значимый контракт, а polymorphism позволяет разным объектам удовлетворять этому контракту.

### Как работает

Python часто использует duck typing: caller зависит от доступного поведения, а не от конкретного дерева наследования. ABC и Protocol делают договор явным, когда это нужно.


### Важный нюанс / ограничение

Начальный underscore обозначает непубличный API, но не является контролем доступа; инварианты всё равно защищают методами, properties и тестами.

### Где используется в backend

Service может принять любой notifier с методом `send`: в тесте передаётся fake, а в production — реальный provider.

## Модель понимания

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- practical Python meaning
- duck typing
- contracts
- avoid Java-style ceremony

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Encapsulation, abstraction and polymorphism: отдельный пример

```python
class JsonRenderable:
    def render(self):
        raise NotImplementedError

class User(JsonRenderable):
    def render(self):
        return {"type": "user"}

def response(item: JsonRenderable):
    return item.render()

print(response(User()))
```

Polymorphism позволяет caller работать через behavior contract, не проверяя конкретный класс.

## Типичные ошибки

### Ошибка 1

Проверка `type(obj) is ConcreteClass` запрещает корректные замены и ломает polymorphism.

## Практика

**A · Предсказание результата.** Измени один input в примере `practical Python meaning` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `duck typing`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `practical Python meaning`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Encapsulation, abstraction and polymorphism за 45–60 секунд и назови одно ограничение.

## Предсказание результата кода

### super следует MRO

```python
class A:
    def name(self): return 'A'
class B(A):
    def name(self): return 'B>' + super().name()
class C(B): pass
print(C().name())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
B>A
```

super в B продолжает поиск после B в MRO фактического класса C.

Типичная ошибка мышления: `mro`.

</details>

## Вопросы с собеседований

### Основной вопрос

Что такое Encapsulation, abstraction and polymorphism и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Encapsulation объединяет состояние и поведение, abstraction показывает значимый контракт, а polymorphism позволяет разным объектам удовлетворять этому контракту.

### Нормальный ответ уровня Junior

> Encapsulation объединяет состояние и поведение, abstraction показывает значимый контракт, а polymorphism позволяет разным объектам удовлетворять этому контракту. Python часто использует duck typing: caller зависит от доступного поведения, а не от конкретного дерева наследования. ABC и Protocol делают договор явным, когда это нужно. Важное ограничение: Начальный underscore обозначает непубличный API, но не является контролем доступа; инварианты всё равно защищают методами, properties и тестами.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?**

Проверка `type(obj) is ConcreteClass` запрещает корректные замены и ломает polymorphism.

## Критерии хорошего ответа

### Что обязательно упомянуть

- practical Python meaning
- duck typing
- contracts
- avoid Java-style ceremony

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Проверка `type(obj) is ConcreteClass` запрещает корректные замены и ломает polymorphism.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?

## Задача

Сделай короткую письменную практику по теме **Encapsulation, abstraction and polymorphism**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Encapsulation объединяет состояние и поведение, abstraction показывает значимый контракт, а polymorphism позволяет разным объектам удовлетворять этому контракту.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Проверка `type(obj) is ConcreteClass` запрещает корректные замены и ломает polymorphism.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
