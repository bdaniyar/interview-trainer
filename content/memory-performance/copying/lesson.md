# Shallow and deep copy

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Shallow and deep copy**, а не только запомнить термин;
- прочитать и изменить короткий пример для `slicing`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Копирование создаёт отдельный объект, но глубина копии определяет, останутся ли общими вложенные объекты. Shallow copy отделяет только внешний контейнер; deep copy пытается скопировать весь достижимый object graph.

### Как работает

`list.copy()`, срез `[:]`, `dict.copy()` и `copy.copy()` создают новый внешний объект и переносят в него те же references на элементы. `copy.deepcopy()` идёт рекурсивно и хранит memo, чтобы не копировать один объект несколько раз и обрабатывать циклы.


### Пример

```python
source = {"roles": ["reader"]}
shallow = source.copy()
shallow["roles"].append("writer")

print(source["roles"])
# ['reader', 'writer']
```

### Важный нюанс / limitation

`deepcopy` не делает автоматически корректную доменную копию: соединения, файловые дескрипторы, ORM entities и shared caches часто нельзя или не нужно дублировать. Иногда правильнее собрать новый объект явно.

### Где используется в backend

При нормализации вложенного JSON shallow copy может оставить общий список ролей; mutation копии тогда изменит исходный payload.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- видеть разницу shallow/deep
- предсказывать nested mutation
- знать `copy.copy` и `copy.deepcopy`

### Полезно

- понимать memo и циклические ссылки на уровне идеи

### Можно не учить глубоко

- внутренний dispatch table модуля `copy`

## Code examples

### Shallow and deep copy: отдельный пример

```python
from copy import copy, deepcopy

source = {"profile": {"roles": ["reader"]}}
shallow = copy(source)
deep = deepcopy(source)
source["profile"]["roles"].append("writer")

print(shallow["profile"]["roles"])
print(deep["profile"]["roles"])
```

Shallow copy разделяет вложенный graph, а deep copy рекурсивно создаёт независимые containers.

## Common mistakes

### Ошибка 1

Считать `payload.copy()` независимой копией всех вложенных данных.

### Ошибка 2

Применять `deepcopy()` к ORM graph вместо явного DTO/serialization boundary.

## Practice

**A · Code prediction.** Измени список внутри shallow copy и предскажи исходный payload.

**C · Rewrite.** Собери новую API-модель явно вместо безусловного `deepcopy` ORM-объекта.

**D · Small task.** Реализуй функцию, которая копирует dict и отдельно копирует список `roles`.

## Code prediction

### Shallow copy

```python
source = {'roles': ['reader']}
copy = source.copy()
copy['roles'].append('writer')
print(source['roles'])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
['reader', 'writer']
```

Копия отделила внешний dict, но вложенный list остался общим.

Misconception: `shallow-copy`.

</details>

## Debugging practice

### Shallow copy

**Сценарий:** dict.copy не изолировал nested roles.

**Rubric:** Outer container новый, nested object общий; selective/deep copy по ownership.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Чем shallow copy отличается от deep copy?

### Follow-up

Почему `deepcopy` может быть плохим выбором для SQLAlchemy model?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Shallow copy создаёт новый внешний контейнер, но делит вложенные объекты; deep copy рекурсивно копирует graph.

### Нормальный Junior answer

> При shallow copy внешний list или dict новый, а его элементы — те же объекты. Поэтому изменение вложенного списка видно и в оригинале. `deepcopy` рекурсивно копирует graph, но дороже и не всегда соответствует смыслу domain data. Для сложных объектов я предпочту явное построение нужной копии.

### Углубление / follow-up

**Почему `deepcopy` может быть плохим выбором для SQLAlchemy model?**

ORM entity связана с Session, lazy relationships и identity map; механическое копирование graph не создаёт корректную новую запись и может загрузить лишние данные.

## Expected answer rubric

### Must mention

- видеть разницу shallow/deep
- предсказывать nested mutation
- знать `copy.copy` и `copy.deepcopy`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Считать `payload.copy()` независимой копией всех вложенных данных.
- пересказ одного определения без механизма или примера.

### Follow-up

- Почему `deepcopy` может быть плохим выбором для SQLAlchemy model?

## Задача

### Изолировать вложенный payload

Верни независимую глубокую копию payload. Мутация вложенных list/dict результата не должна менять оригинал.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Shallow copy создаёт новый внешний контейнер, но делит вложенные объекты; deep copy рекурсивно копирует graph.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Считать `payload.copy()` независимой копией всех вложенных данных.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
