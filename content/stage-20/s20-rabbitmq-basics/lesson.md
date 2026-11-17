# RabbitMQ basics

## Суть

Producer RabbitMQ публикует в exchange. Exchange маршрутизирует сообщение в queue по binding и routing key. Consumer получает delivery из queue; broker удерживает unacked message до подтверждения или потери соединения.

## Учебные цели

Проследить маршрутизацию exchange → queue → consumer. Наблюдать redelivery после разрыва соединения, различать producer confirm и consumer ack и отправить отклонённое сообщение в DLQ.

## Зачем это нужно backend-разработчику

Прочитайте `brokers_smoke.py` и отметьте confirm_delivery, auto_ack=False, закрытие connection и basic_nack. В своей копии замените nack на requeue=True: assertion dead queue должен упасть, а исходная очередь будет снова содержать сообщение. Объясните риск горячего poison loop.

## Теория

### Что это

Producer RabbitMQ публикует в exchange. Exchange маршрутизирует сообщение в queue по binding и routing key. Consumer получает delivery из queue; broker удерживает unacked message до подтверждения или потери соединения.

### Как работает

В lab используется default exchange для direct routing по имени queue. Durable queue и persistent delivery_mode=2 описывают сохранность, publisher confirms подтверждают broker acceptance. Consumer basic_get(auto_ack=False) требует явного basic_ack delivery_tag, принадлежащего текущему channel. После закрытия connection без ack broker снова делает сообщение доступным.

redelivered — полезный признак повторной выдачи, но идемпотентность нельзя строить только на нём: producer тоже может опубликовать логический дубль с новым delivery. Нужен business/message ID. После permanent failure basic_nack(requeue=False) направляет сообщение в настроенный DLX; без DLX оно может быть удалено.

В тесте отдельный direct DLX маршрутизирует в dead queue, headers x-death содержит reason=rejected. Ack в dead queue завершает эту delivery. В production настройка DLX через policy гибче hardcoded queue arguments. Consumer prefetch ограничивает unacked deliveries, а не автоматически скорость бизнес-операции.

### Важный нюанс / ограничение

Publisher confirm не равен consumer success. Consumer ack до business COMMIT даёт окно потери; ack после него даёт окно дубля. Сохранность очереди не отменяет idempotent consumer.

## Модель понимания

Отмечайте отдельно приём работы, владение ею и COMMIT эффекта. Для каждого сбоя подпишите, какие данные уже устойчивы и кто имеет право повторить операцию. Сопоставьте этот путь с конкретным тестом проекта, а не только с названием framework.

## Что нужно знать на Junior

### Обязательно

Exchange маршрутизирует, queue хранит, consumer обрабатывает. Prefetch ограничивает неподтверждённые доставки. Ack, nack с requeue и dead lettering задают разные дальнейшие пути; причины отклонения и лимит повторов должны быть видны оператору.

## Примеры кода

```sh
docker compose -f projects/durable_queue/compose.brokers.yml logs --tail=20 rabbit
```

После scripts/test_queue_brokers.sh стенд удаляется, поэтому для ручного изучения сначала поднимите его по README. Автоматическая проверка получает b"work", теряет unacked connection, получает redelivered=True, отправляет nack и читает тот же body из dead queue. Очереди имеют случайные имена и удаляются после проверки.

Полный исполняемый проект и команды проверки: `projects/durable_queue/README.md`. Docker-практика выполняется отдельно от четырёхсекундного networkless Python Runner.

## Типичные ошибки

Ack до business COMMIT оставляет окно потери. Бесконечный nack(requeue=True) превращает poison message в горячий цикл. Увеличение prefetch без анализа времени обработки удерживает работу у медленного consumer. DLQ сама по себе не исправляет payload и не задаёт безопасный повтор.

## Практика

Прочитайте `brokers_smoke.py` и отметьте confirm_delivery, auto_ack=False, закрытие connection и basic_nack. В своей копии замените nack на requeue=True: assertion dead queue должен упасть, а исходная очередь будет снова содержать сообщение. Объясните риск горячего poison loop.

## Вопросы с собеседований

1. Что произойдёт с unacked delivery после потери connection?
2. Куда ведёт nack(requeue=False)?

## Хорошие ответы

<details>
<summary>Раскрыть ответы</summary>

Broker делает её доступной для повторной доставки; consumer должен быть готов к дублю бизнес-операции.

В настроенный dead-letter exchange/queue, либо к удалению, если DLX отсутствует. Это не автоматическое исправление poison message.

</details>

## Критерии хорошего ответа

<details>
<summary>Раскрыть критерии</summary>

Укажите transaction boundary, ownership, возможный повтор и наблюдаемое состояние после сбоя. Назовите конкретное ограничение этого механизма и соответствующий исполняемый тест.

</details>

## Задача

Прочитайте `brokers_smoke.py` и отметьте confirm_delivery, auto_ack=False, закрытие connection и basic_nack. В своей копии замените nack на requeue=True: assertion dead queue должен упасть, а исходная очередь будет снова содержать сообщение. Объясните риск горячего poison loop.

Внесите изменение в свою копию проекта и запустите соответствующий integration test. Критерий успеха — сохранённый invariant и ожидаемый failure при намеренно сломанной границе; текстовое объяснение автоматически не оценивается.

## Шпаргалка

Confirm закрывает producer → broker, ack — broker → consumer. Business COMMIT находится в приложении. Повтор после потери ack требует идемпотентного effect. DLX маршрутизирует отклонённые сообщения; DLQ нуждается в диагностике и явном retry contract.

## Источники

- [RabbitMQ 4.1: consumer acknowledgements](https://www.rabbitmq.com/docs/4.1/confirms).
- [RabbitMQ 4.1: dead letter exchanges](https://www.rabbitmq.com/docs/4.1/dlx).

Официальные секции сверены 2026-11-16. Исполнение проекта: PostgreSQL 17.11, SQLAlchemy 2.0.43, FastAPI 0.116.1; comparison Celery 5.5.3, Redis 7.4.12, RabbitMQ 4.1.8, Kafka 4.1.0. Точные pins находятся в проекте. Страница latest может меняться: проверенный код и версии указаны отдельно.
