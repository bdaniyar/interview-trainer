# Object lifetime

Материал урока пока не добавлен. Структура уже готова для будущего импорта.

## Что нужно изучить

- `lifetime`
- `finalization`

> [!NOTE]
> Пришли материал с заголовками `TOPIC:` и `MATERIAL:` — он будет встроен в этот урок без создания дубля.

## Задача

Задача и hidden tests будут добавлены позже.

## Code prediction

### Cycle не означает немедленное удаление

```python
a = []
a.append(a)
print(a[0] is a)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
True
```

Список может ссылаться на себя; цикл обрабатывает cyclic GC, а identity сохраняется.

Misconception: `reference-cycle`.

</details>

## Предсказание результата кода

### Cycle не означает немедленное удаление

```python
a = []
a.append(a)
print(a[0] is a)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
True
```

Список может ссылаться на себя; цикл обрабатывает cyclic GC, а identity сохраняется.

Типичная ошибка мышления: `reference-cycle`.

</details>
