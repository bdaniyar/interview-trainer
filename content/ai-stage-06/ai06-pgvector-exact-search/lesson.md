# PostgreSQL и pgvector: точный поиск

В PostgreSQL можно хранить числовое представление фрагмента рядом с ключом его источника. Поиск выбирает ближайшие векторы во множестве документов, доступных конкретному пользователю.

## Учебные цели

- Запустить PostgreSQL 17 и pgvector в отдельном P4.
- Объяснить операторы и проверить exact выборку вручную.

## Теория

Расширение pgvector добавляет тип `vector(n)`. Оно устанавливается доверенной миграцией с отдельным пользователем. `a <=> b` — cosine distance, `a <-> b` — L2, `a <#> b` — отрицательный inner product, чтобы поиск мог сортировать по возрастанию. Cosine similarity вычисляется как `1 - (a <=> b)`.

SQL связывает fragment с tenant, document version и embedding space. ACL здесь — список разрешённых пользователей. В запросе совпадают tenant и embedding space, версия активна, документ не удалён, а caller — владелец либо имеет grant внутри tenant. Параметры psycopg передаются отдельно от SQL. Названия таблиц фиксированы в коде. Exact baseline вычисляет distance для каждого разрешённого вектора. В P4 materialized CTE отделяет множество кандидатов от сортировки, поэтому ANN не подменяет скан.

## Модель понимания

Вход query [1,0]. У владельца есть два разрешённых фрагмента того же направления. Соседний tenant хранит третий с таким же score. Сначала определяем доступные кандидаты, затем сортируем равные по document ID и chunk ID. Права не зависят от score.

## Что нужно знать на Junior

Проверь реальный план и версию расширения. Вдобавок к размерности зафиксируй модель и её revision. Runtime роль не выдаёт себе DDL. SQL Lab в браузере остаётся в своём контейнере.

## Примеры кода

```python
from math import hypot
query = (1, 0)
for v in ((2, 0), (0, 3), (-1, 0)):
    distance = 1 - sum(a*b for a,b in zip(query,v)) / (hypot(*query)*hypot(*v))
    print(distance)
```

Вывод `0.0, 1.0, 2.0`. P4 сравнивает реальные SQL distance и IDs с независимым Python расчётом на 16-мерных фикстурах.

## Типичные ошибки

- Сортировать cosine distance по убыванию.
- Разрешить модели или запросу выбрать tenant.
- Проверять ACL только после поиска top-k.

## Практика

Вход: три разрешённых и две чужие строки, k=3. Чужие на втором и третьем месте глобального плана. Сколько строк вернёт поиск, если отбросить их после LIMIT?

<details>
<summary>Сверить разбор упражнения</summary>

Останется одна строка; две законные строки потеряны. Exact baseline сначала ограничивает множество доступными строками.

</details>

## Вопросы с собеседований

1. Почему миграция и поисковая роль отдельные?
2. Как доказать exact ranking?
3. Почему размерность не равна embedding space?

## Хорошие ответы

**Почему миграция и поисковая роль отдельные?**

Установка расширения и изменение схемы требуют повышенных прав. Поиск использует фиксированный SQL и выданные права на таблицы.

**Как доказать exact ranking?**

Сверить реальные IDs и расстояния с независимым полным перебором. Тест должен менять ACL и равные distance.

**Почему размерность не равна embedding space?**

Две модели могут возвращать вектор одинакового размера с разными координатами. Сохраняй model, revision и normalization.

## Критерии хорошего ответа

Назови предикаты tenant, owner и version, покажи знак cosine distance и сравни SQL-сортировку с полным перебором на двух равных расстояниях.

## Задача

Реализуй `exact(scope, query, rows, k)`. DTO в contracts.py. При отсутствии may_read подними PermissionError. Проверяй tenant, space, active_version, deleted и права owner/readers до чтения вектора. Для разрешённых строк валидируй непустую конечную ненулевую форму без bool, совпадение размерности и k как строгий int >=0. Верни список (document, version, chunk_id, cosine distance), сортировка по distance/document/chunk ID, первые k. Пример Run выдаёт guide с distance 1.0. Браузерный Check проверяет только Python oracle. Для реальной практики запусти `docker compose -f projects/vector_search/compose.yaml up -d --wait`, затем `python -m projects.vector_search.cli seed`, `python -m projects.vector_search.cli exact` и `python -m pytest -o addopts='' -q projects/vector_search/tests`. Окружение и команды описаны в [P4](https://github.com/bdaniyar/interview-trainer/tree/main/projects/vector_search).

## Шпаргалка

### Краткий конспект

Exact выбирает кандидатов по scope, tenant, ACL, актуальной версии и space, вычисляет distance и стабильно сортирует. Для [1,0] и [0,3] distance=1. В pgvector это `<=>`, а runtime ведёт параметры отдельно от текста SQL.

- Можно ли передать имя таблицы как обычное значение psycopg?
- Что добавить для совпавших оценок?
- Когда старый chunk должен исчезнуть из поиска?

<details>
<summary>Ответы для самопроверки</summary>

**Можно ли передать имя таблицы как обычное значение psycopg?**

Нет, value placeholders параметризуют данные.

**Что добавить для совпавших оценок?**

Стабильную сортировку по document ID и chunk ID.

**Когда старый chunk должен исчезнуть из поиска?**

После атомарного переключения active_version или tombstone.

</details>

## Источники

- Querying, HNSW, filtering. PG17 + pgvector 0.8.2. Проверено 2026-11-24. [PGV](https://github.com/pgvector/pgvector/tree/v0.8.2)
- EXPLAIN ANALYZE. PostgreSQL 17 plans. Проверено 2026-11-24. [PLAN](https://www.postgresql.org/docs/17/using-explain.html)
