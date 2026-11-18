# Transaction Lab — отдельный PostgreSQL профиль

`pg-transaction-v1` — локальный SQL-only Run/Check и controlled timeline на
настоящем PostgreSQL 17.11. В Pythoria Transaction Lab открывается в уроках
10.25 и в девяти уроках Stage 11, включая 11.17. CLI остаётся способом
запуска тех же сценариев из терминала.

Нажмите «Открыть сессии» и загрузите пример блокировки. Запустите A, затем B.
Пока B ждёт, нажмите COMMIT в A. Timeline показывает порядок команд и связь
ожидания, которую PostgreSQL сообщил через `pg_blocking_pids`. На телефоне
переключайтесь между A, B, Timeline и «Данные». Для немедленного эксперимента
вкладка «Данные» показывает снимок подтверждённых строк из третьего соединения.

Run сохраняет транзакцию между командами. Сессии живут до 60 секунд, открытая
транзакция без команд — до 5 секунд, ожидание блокировки — до 1,5 секунды.
Команды для наблюдения лучше подготовить заранее. Для анализа в своём темпе
запустите готовый сценарий: он воспроизводит порядок операций в свежей базе.

Check A проверяет черновик A в независимых временных базах. Веб-приложение
сохраняет завершение и попытки в SQLite с отдельным ID задания. Повторная
проверка и Reset не стирают завершение. Черновики A и B хранятся в браузере.
CLI выводит JSON. Web и CLI Check не начисляют XP.

## Запуск

Активируйте dev-окружение проекта (`requirements-dev.txt`, Python 3.11+), затем
из корня репозитория соберите закреплённую базу и отдельный образ:

```sh
docker compose build sql-sandbox
docker build -t pythoria-transaction-sandbox:phase8b -f transaction_lab/Dockerfile .
python3 -m transaction_lab.cli scenario read-committed
python3 -m transaction_lab.cli scenario repeatable-read
python3 -m transaction_lab.cli scenario blocking-update
python3 -m transaction_lab.cli scenario nowait
python3 -m transaction_lab.cli scenario skip-locked
python3 -m transaction_lab.cli scenario deadlock
python3 -m transaction_lab.cli scenario serializable
python3 -m transaction_lab.cli scenario exclusion
```

Каждая команда создаёт новый networkless sandbox с tmpfs и удаляет его в finally.
Старый образ распознаётся по fingerprint фактических policy/bootstrap/executor/
fixtures; в этом случае CLI требует пересборку. Нет DSN, production credentials,
произвольного command/image/mount или сетевого SQL endpoint от студента.

В JSON timeline `session=A/B` обозначают разные соединения. Observer — отдельное
соединение для состояния и lock dependency. В blocking/deadlock/exclusion порядок
подтверждается `pg_blocking_pids`, а не фиксированными sleeps. Отдельные сценарии
`rollback-savepoint`, `mvcc`, `lost-update`, `indexes` показывают откат, старую
версию, намеренно потерянный инкремент и plain EXPLAIN соответственно.
`indexes` не является демонстрацией изоляции и не обещает ускорение на tiny data.

## Два graded упражнения

Скопируйте starter в собственный `query.sql`, прочитайте условие в уроке и
напишите решение. Ниже приведены команды проверки, не готовые ответы:

```sh
cp transaction_lab/examples/dml.sql query.sql
python3 -m transaction_lab.cli run --exercise dml --file query.sql
python3 -m transaction_lab.cli check --exercise dml --file query.sql
```

- `pg.write.10.25.status-v1`, revision 1: изменить только orders.id=10 на paid,
  вернуть id,status. Если заказа нет — пустой результат и отсутствие изменений.
- `pg.tx.11.17.booking-v1`, revision 1: два запроса пытаются забронировать одну
  единицу inventory.id=1; вернуть request_key,room_id либо пустой конфликт.
  Используйте точный SQL-литерал `'REQUEST_KEY'`; coordinator подставляет два
  разных синтетических ключа. Starter: `examples/booking.sql`.

У каждого Check шесть свежих баз. Проверяются typed results и итог **всех семи
таблиц**, включая отсутствие изменений чужих orders/rooms. В booking проверяются
оба ответа, единственная новая active reservation, остаток и сохранность прежних
строк. Публичный Run показывает собственные before/after и SQLSTATE; Check
возвращает только итоговые счётчики и безопасный feedback, без hidden rows/cases.
Failed Check завершает CLI с exit code 1. JSON можно сохранить в локальный файл.

## Безопасность

- Контроллер работает локально с Docker SDK; socket не попадает в sandbox.
- PostgreSQL доступен только через Unix socket; Docker network=none, без bind
  mounts и persistent volumes. Данные синтетические, основной volume не читается.
- Read-only root, 512 MiB RAM/swap, 1 CPU, 128 PIDs, dropped capabilities и
  no-new-privileges. PostgreSQL запускается non-root, SQL executor — UID 65532.
- Peer authentication связывает executor с non-superuser student. Нет
  CREATEDB/CREATEROLE/replication/bypassrls/TEMP/schema CREATE/ownership.
- Профиль разрешает ограниченные SELECT, DML по orders/inventory/reservations,
  BEGIN/COMMIT/ROLLBACK/SAVEPOINT, три уровня изоляции, row locks и plain EXPLAIN
  SELECT. DDL, COPY/PROGRAM, SET/RESET/ROLE, arbitrary schemas/functions,
  prepared transactions и произвольные extension запрещены AST. DB permissions
  дополнительно запрещают DDL, доступ к файлам/чужим ролям и запись в read-only таблицы.
- Trusted exclusion scenario имеет отдельную synthetic int4range таблицу slots;
  её диапазоны не открывают произвольные типы или DDL в student policy.
- Не более 16 statements/32 KiB SQL, 500 rows/1 MiB result, 64 KiB cell. SQL
  statement deadline 3 s, lock timeout 1.5 s, idle transaction 5 s, transaction
  lifetime 15 s, внешняя операция 20 s. Весь контейнер имеет watchdog 60 s.
- Незавершённый BEGIN откатывается. Закрытие/ошибка coordinator удаляет контейнер;
  watchdog и auto-remove убирают orphan после падения controller. Один CLI
  обслуживает одну попытку за раз; это trusted single-user local tool, не hosted API.

## Проверки

```sh
python3 -m pytest transaction_lab/tests/test_transaction_policy.py
SQL_DOCKER_TESTS=1 python3 -m pytest transaction_lab/tests/integration -v
```

Интеграции используют реальные независимые соединения, ограничения, deadlines и
одноразовые базы. Проверяются RC/RR, MVCC, 40001, 40P01, 55P03, 23P01,
FK/UNIQUE/CHECK, SAVEPOINT recovery, booking races, точное состояние, контроль
привилегий, cancellation и orphan TTL. Планировочные стоимости и конкретный
победитель deadlock/booking не фиксируются как часть контракта.

Контроллер Web Lab допускает одну учебную базу и одну длительную проверку или
готовый сценарий одновременно. В базе разрешено по одной операции на A и B.
При Reset контейнер удаляется и выдаётся новое поколение той же сессии. После
истечения срока создайте новую базу. Начало работы контроллера очищает только
его собственные контейнеры. Watchdog работает даже при завершении контроллера.

Веб-проверка и перезапуск приложения проверяются из корня проекта командой
`scripts/test_transaction_workspace.sh`. Она поднимает временный тестовый
проект и отдельное хранилище SQLite. Сценарий Chrome запускается через
`node scripts/smoke_sql_browser.mjs --transactions-only` на тестовом стеке.

Источники механизма ожиданий и сроков проверены 18 ноября 2026 года.
[PostgreSQL 17, session information](https://www.postgresql.org/docs/17/functions-info.html#FUNCTIONS-INFO-SESSION-TABLE),
[PostgreSQL 17, statement behavior](https://www.postgresql.org/docs/17/runtime-config-client.html#RUNTIME-CONFIG-CLIENT-STATEMENT).

Фактические проверки и границы доставки: [Phase 8B verification](../docs/PHASE8B_VERIFICATION.md).
