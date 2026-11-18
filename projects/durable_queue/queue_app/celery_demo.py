"""Optional real Celery comparison; pure task, no exactly-once effect claim."""

import os
from celery import Celery

app = Celery(
    "comparison",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_RESULT_BACKEND"],
)
app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    task_time_limit=5,
    broker_transport_options={"visibility_timeout": 30},
    result_backend_transport_options={"visibility_timeout": 30},
    visibility_timeout=30,
)


@app.task(name="comparison.sum_squares")
def sum_squares(n):
    if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 100000:
        raise ValueError("n must be 0..100000")
    return sum(i * i for i in range(n + 1))
