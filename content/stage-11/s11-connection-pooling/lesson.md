# Connection pooling

## Учебные цели

Рассчитать лимит подключений для приложения с несколькими процессами.
Открывать отдельную AsyncSession на запрос, завершать транзакцию на всех
ветках и отличать исчерпание пула от ожидания PostgreSQL.

## Теория

### Что это

Пул держит ограниченный набор соединений и выдаёт одно из них на время работы с БД.

### Как работает

Установка соединения с PostgreSQL требует времени. Сервер хранит состояние
соединения и выделяет ему ресурсы. Пул позволяет переиспользовать уже открытые
соединения. Checkout выдаёт одно из них запросу, check-in возвращает его.
Закрытие SQLAlchemy Session или Connection обычно возвращает соединение в
пул, хотя само сетевое подключение может остаться открытым.

В QueuePool `pool_size` задаёт число постоянно сохраняемых соединений,
`max_overflow` — сколько дополнительных можно открыть при нагрузке.
`pool_timeout` ограничивает ожидание выдачи после исчерпания доступных мест.
Overflow закрывается при возврате, если пул уже заполнен. AsyncEngine с
совместимым сетевым драйвером обычно использует AsyncAdaptedQueuePool.
При настройке 5 + 2 и четырёх Uvicorn workers верхняя оценка для одного
такого engine на процесс — 28 соединений. Добавьте фоновые jobs, миграции,
другие реплики и место для администрирования.

AsyncSession — изменяемый объект, связанный с состоянием транзакции.
В параллельных asyncio-задачах каждому use case нужна своя сессия. FastAPI
dependency с yield может передать сессию запросу и закрыть её в cleanup.
Выберите границу транзакции в use case. Долгий HTTP внутри открытой
транзакции удерживает соединение, иногда и locks. Непрочитанный стрим,
которому нужна БД, тоже продлевает checkout.

### Важный нюанс / ограничение

Несколько workers создают независимые engines. Максимум соединений складывается вместе с фоновыми процессами и репликами.

## Модель понимания

Разложите запрос на очередь за checkout, работу PostgreSQL и check-in. Если ждёт checkout, запрос ещё не появился в очереди блокировок PostgreSQL.

## Что нужно знать на Junior

### Обязательно

Один engine на процесс, отдельная AsyncSession на запрос или задачу. Закрывайте её и заканчивайте транзакцию на успешном и ошибочном путях.

## Примеры кода

Практика проверяется командой `scripts/test_stage11_examples.sh` на синтетической PostgreSQL 17.11. Запускайте изменения в отдельной учебной базе.

В учебном проекте передайте DSN отдельной PostgreSQL-базы при создании app.
Пример читает 42 как integer. Commit для этого чтения не требуется. Контекст
закроет сессию и откатит её незавершённую транзакцию даже при исключении.

```python
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def make_app(dsn: str) -> FastAPI:
    engine = create_async_engine(
        dsn, pool_size=1, max_overflow=0, pool_timeout=0.5, pool_pre_ping=True
    )
    sessions = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(lifespan=lifespan)

    async def db():
        async with sessions() as session:
            yield session

    @app.get("/value")
    async def read_value(session: AsyncSession = Depends(db)):
        value = await session.scalar(text("SELECT CAST(42 AS integer)"))
        return {"value": value}

    return app
```

`GET /value` возвращает `{"value": 42}`. Повторный запрос работает с тем же
лимитом после возврата первого соединения. В обработчике записи используйте
`async with session.begin():`: выход без ошибки фиксирует изменения, исключение
приводит к rollback до возврата соединения.

### PgBouncer и диагностика

PgBouncer размещает пул между приложением и PostgreSQL. В session pooling
серверное соединение закреплено за клиентским на весь клиентский сеанс.
В transaction pooling серверное соединение закреплено на время транзакции.
Состояние, которое должно пережить транзакцию, в этом режиме требует проверки
совместимости. Примеры — сессионные SET, временные таблицы и prepared statements.
Проверяйте матрицу PgBouncer для нужной функции и конфигурации драйвера.

Измеряйте время checkout, число checked out и возраст открытой транзакции.
В PostgreSQL `pg_stat_activity` показывает `state`, `xact_start`, тип и событие
ожидания. Различайте очередь приложения за свободным соединением, серверное
ожидание lock и длительное выполнение запроса. Контроль размера пула не
исправляет утечку соединения.

## Типичные ошибки

Создавать engine на каждый запрос. Передавать одну AsyncSession в
`asyncio.gather`. Компенсировать утечку большим overflow. Держать
сессию после ошибки без rollback и сразу выполнять второй запрос.
Рассчитывать лимит только для одного процесса, когда запущено несколько.

## Практика

В проекте `projects/pool_lab` исправьте утечку сессии SQLAlchemy и пропустите через ограниченный пул два одновременных HTTP-запроса. Проверьте откат при ошибке и успешный запрос после освобождения соединения. Запуск и контракт описаны в README проекта.

В отдельной копии проекта при `pool_size=1, max_overflow=0` удержите одно
соединение контролируемым событием. Второй запрос должен получить
`sqlalchemy.exc.TimeoutError` до освобождения места. Завершите первую
транзакцию и подтвердите, что следующий запрос возвращает 42. Повторите
с исключением внутри первого use case и проверьте, что место снова доступно.
Измерьте число checkout/check-in, не увеличивая лимит пула.

## Вопросы с собеседований

1. Сколько соединений может занять приложение при четырёх процессах и настройке 5 + 2?
2. Как отличить ошибку checkout от блокировки строки?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

До 28 для четырёх независимых engines с таким лимитом, плюс потребители
за пределами этих engines. Пул каждого процесса имеет собственный бюджет.

При checkout соединение ещё не получено. При блокировке запрос уже
в PostgreSQL и виден в статистике ожиданий. Проверяйте pool wait time,
состояние соединений и server wait events отдельно.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Покажите верхний предел подключений, место checkout и путь rollback. Объясните, что наблюдает приложение, а что видно в pg_stat_activity.

</details>

## Задача

В учебном приложении добавьте маршрут диагностики checked-out connections в тестовой сборке. Проверьте переходы 0 → 1 → 0 при выполнении запроса и при исключении. Не публикуйте внутреннюю диагностическую статистику в обычном API.

## Шпаргалка

Engine на процесс, AsyncSession на use case, транзакция короткая.
Считайте лимит по всем репликам. При timeout сначала выясните,
где ждёт запрос, и проверьте возврат соединения на ошибочном пути.

## Источники

- [SQLAlchemy 2.0, Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html).
- [SQLAlchemy 2.0, AsyncSession with concurrent tasks](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks).
- [FastAPI, Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
- [PgBouncer, feature map for pooling modes](https://www.pgbouncer.org/features.html).

Секции сверены 18 ноября 2026 года. Проверенные версии стенда указаны в документации Phase 9B.
