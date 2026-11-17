"""Real Redis/Celery and RabbitMQ delivery checks; no mocks or public ports."""

import json
import os
from threading import Event
from time import monotonic
from uuid import uuid4

import pika
import redis
from .celery_demo import sum_squares


def main():
    client = redis.Redis.from_url(
        os.environ["REDIS_URL"], decode_responses=True, socket_timeout=2
    )
    assert client.ping()
    queue = "learning-" + uuid4().hex
    client.rpush(queue, "first", "second")
    assert client.blpop(queue, timeout=1) == (queue, "first")
    assert client.blpop(queue, timeout=1) == (queue, "second")
    assert client.blpop(queue, timeout=1) is None
    result = sum_squares.delay(10)
    assert result.get(timeout=20) == 385
    result.forget()
    params = pika.ConnectionParameters(
        "rabbit",
        credentials=pika.PlainCredentials("learner", "synthetic-local-only"),
        socket_timeout=3,
        blocked_connection_timeout=3,
    )
    conn = pika.BlockingConnection(params)
    channel = conn.channel()
    name = "learning-" + uuid4().hex
    dead = name + "-dead"
    exchange = name + "-dlx"
    channel.exchange_declare(exchange=exchange, exchange_type="direct", durable=True)
    channel.queue_declare(dead, durable=True)
    channel.queue_bind(dead, exchange, "dead")
    channel.queue_declare(
        name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": exchange,
            "x-dead-letter-routing-key": "dead",
        },
    )
    channel.confirm_delivery()
    channel.basic_publish(
        "",
        name,
        b"work",
        properties=pika.BasicProperties(delivery_mode=2),
        mandatory=True,
    )
    method, _, body = channel.basic_get(name, auto_ack=False)
    assert method and body == b"work"
    conn.close()  # Deliberately lose an unacknowledged delivery.
    conn = pika.BlockingConnection(params)
    channel = conn.channel()
    try:
        deadline = monotonic() + 5
        while True:
            method, _, body = channel.basic_get(name, auto_ack=False)
            if method:
                break
            assert monotonic() < deadline
            Event().wait(0.02)
        assert method.redelivered and body == b"work"
        channel.basic_nack(method.delivery_tag, requeue=False)
        deadline = monotonic() + 5
        while True:
            method, properties, body = channel.basic_get(dead, auto_ack=False)
            if method:
                break
            assert monotonic() < deadline
            Event().wait(0.02)
        assert (
            body == b"work" and properties.headers["x-death"][0]["reason"] == "rejected"
        )
        channel.basic_ack(method.delivery_tag)
        assert channel.basic_get(name)[0] is None and channel.basic_get(dead)[0] is None
    finally:
        channel.queue_delete(name)
        channel.queue_delete(dead)
        channel.exchange_delete(exchange)
        conn.close()
        client.close()
    print(
        json.dumps(
            dict(
                redis_lists=True,
                celery_real_worker_and_result=True,
                rabbit_publisher_confirm=True,
                rabbit_unacked_redelivery=True,
                rabbit_dead_letter=True,
            )
        )
    )


if __name__ == "__main__":
    main()
