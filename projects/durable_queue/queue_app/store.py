from dataclasses import dataclass
from hashlib import sha256
import json
from uuid import uuid4

from sqlalchemy import create_engine, text


class LostLease(RuntimeError):
    pass


class IdempotencyConflict(ValueError):
    pass


def backoff(attempt, base=0.1, cap=30.0):
    if (
        isinstance(attempt, bool)
        or not isinstance(attempt, int)
        or not 1 <= attempt <= 8
    ):
        raise ValueError("attempt must be 1..8")
    if not 0 < base <= cap <= 300:
        raise ValueError("invalid retry budgets")
    return min(cap, base * 2 ** (attempt - 1))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(value):
    return sha256(canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class Lease:
    id: object
    worker: str
    generation: int
    attempts: int
    payload: dict


class Store:
    def __init__(self, url):
        self.engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=5,
            connect_args={"connect_timeout": 3},
        )

    def submit(self, key, payload, max_attempts=3, *, after_insert=None):
        if not isinstance(key, str) or not 1 <= len(key) <= 256:
            raise ValueError("invalid idempotency key")
        if (
            isinstance(max_attempts, bool)
            or not isinstance(max_attempts, int)
            or not 1 <= max_attempts <= 8
        ):
            raise ValueError("invalid attempt budget")
        digest = fingerprint(dict(payload=payload, max_attempts=max_attempts))
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        """INSERT INTO jobs(id,idempotency_key,request_hash,payload,max_attempts)
                VALUES(:id,:key,:digest,CAST(:payload AS jsonb),:maximum)
                ON CONFLICT(idempotency_key) DO NOTHING RETURNING *"""
                    ),
                    dict(
                        id=uuid4(),
                        key=key,
                        digest=digest,
                        payload=canonical(payload),
                        maximum=max_attempts,
                    ),
                )
                .mappings()
                .first()
            )
            created = row is not None
            if row is None:
                row = (
                    conn.execute(
                        text("SELECT * FROM jobs WHERE idempotency_key=:key"),
                        dict(key=key),
                    )
                    .mappings()
                    .one()
                )
                if row["request_hash"] != digest:
                    raise IdempotencyConflict("Key already names a different request")
            else:
                if after_insert:
                    after_insert(conn)
                conn.execute(
                    text(
                        "INSERT INTO outbox(id,job_id,kind,payload) VALUES(:id,:job,'job.created',CAST(:payload AS jsonb))"
                    ),
                    dict(
                        id=uuid4(),
                        job=row["id"],
                        payload=canonical(dict(job_id=str(row["id"]))),
                    ),
                )
            return dict(row), created

    def get(self, job):
        with self.engine.connect() as conn:
            row = (
                conn.execute(text("SELECT * FROM jobs WHERE id=:id"), dict(id=job))
                .mappings()
                .first()
            )
            return dict(row) if row else None

    def claim(self, worker, lease_seconds=5):
        if (
            not isinstance(worker, str)
            or not 1 <= len(worker) <= 128
            or not 0.1 <= lease_seconds <= 60
        ):
            raise ValueError("invalid lease")
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """UPDATE jobs SET state='failed',generation=generation+1,worker_id=NULL,
                lease_until=NULL,error='final lease expired' WHERE state='running'
                AND lease_until<=clock_timestamp() AND attempts>=max_attempts"""
                )
            )
            row = (
                conn.execute(
                    text("""WITH picked AS (
                SELECT id FROM jobs WHERE attempts<max_attempts AND
                ((state='queued' AND available_at<=clock_timestamp()) OR
                 (state='running' AND lease_until<=clock_timestamp()))
                ORDER BY available_at,created_at,id FOR UPDATE SKIP LOCKED LIMIT 1
              ) UPDATE jobs j SET state='running',attempts=j.attempts+1,generation=j.generation+1,
                worker_id=:worker,lease_until=clock_timestamp()+:seconds*INTERVAL '1 second'
                FROM picked p WHERE j.id=p.id RETURNING j.*"""),
                    dict(worker=worker, seconds=lease_seconds),
                )
                .mappings()
                .first()
            )
            return (
                Lease(
                    row["id"],
                    worker,
                    row["generation"],
                    row["attempts"],
                    row["payload"],
                )
                if row
                else None
            )

    @staticmethod
    def owner(lease):
        return dict(id=lease.id, worker=lease.worker, generation=lease.generation)

    def heartbeat(self, lease, seconds=5):
        if not 0.1 <= seconds <= 60:
            raise ValueError("invalid lease")
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """UPDATE jobs SET lease_until=clock_timestamp()+:seconds*INTERVAL '1 second'
                WHERE id=:id AND state='running' AND generation=:generation AND worker_id=:worker
                AND lease_until>clock_timestamp() RETURNING id"""
                ),
                self.owner(lease) | dict(seconds=seconds),
            ).first()
            return row is not None

    def finish(self, lease, value):
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """UPDATE jobs SET state='succeeded',worker_id=NULL,lease_until=NULL,
                result=CAST(:value AS jsonb),error=NULL WHERE id=:id AND state='running'
                AND generation=:generation AND worker_id=:worker AND lease_until>clock_timestamp() RETURNING id"""
                ),
                self.owner(lease) | dict(value=canonical(value)),
            ).first()
            if row is None:
                raise LostLease("Completion no longer owns a live lease")
            conn.execute(
                text(
                    "INSERT INTO effects(job_id,value) VALUES(:id,CAST(:value AS jsonb))"
                ),
                dict(id=lease.id, value=canonical(value)),
            )

    def fail(self, lease, *, retryable=True):
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """UPDATE jobs SET
                state=CASE WHEN :retryable AND attempts<max_attempts THEN 'queued' ELSE 'failed' END,
                available_at=clock_timestamp()+:delay*INTERVAL '1 second',worker_id=NULL,lease_until=NULL,
                error='synthetic processing failure' WHERE id=:id AND state='running'
                AND generation=:generation AND worker_id=:worker AND lease_until>clock_timestamp() RETURNING state"""
                ),
                self.owner(lease)
                | dict(retryable=retryable, delay=backoff(lease.attempts)),
            ).first()
            if row is None:
                raise LostLease("Failure no longer owns a live lease")
            return row[0]

    def cancel(self, job):
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """UPDATE jobs SET state='cancelled',generation=generation+1,worker_id=NULL,
                lease_until=NULL WHERE id=:id AND state IN ('queued','running') RETURNING id"""
                ),
                dict(id=job),
            ).first()
            return row is not None

    def claim_event(self, seconds=5):
        if not 0.1 <= seconds <= 60:
            raise ValueError("invalid event lease")
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text("""WITH picked AS (SELECT id FROM outbox WHERE NOT delivered
                AND (lease_until IS NULL OR lease_until<=clock_timestamp())
                ORDER BY created_at,id FOR UPDATE SKIP LOCKED LIMIT 1)
                UPDATE outbox o SET generation=o.generation+1,lease_until=clock_timestamp()+:seconds*INTERVAL '1 second'
                FROM picked p WHERE o.id=p.id RETURNING o.*"""),
                    dict(seconds=seconds),
                )
                .mappings()
                .first()
            )
            return dict(row) if row else None

    def ack_event(self, event):
        with self.engine.begin() as conn:
            return (
                conn.execute(
                    text("""UPDATE outbox SET delivered=true,lease_until=NULL
                WHERE id=:id AND generation=:generation AND NOT delivered AND lease_until>clock_timestamp()
                RETURNING id"""),
                    dict(id=event["id"], generation=event["generation"]),
                ).first()
                is not None
            )

    def receive_effect(self, key, payload):
        digest = fingerprint(payload)
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        """INSERT INTO external_effects(key,request_hash,value)
                VALUES(:key,:hash,CAST(:value AS jsonb)) ON CONFLICT(key) DO NOTHING RETURNING *"""
                    ),
                    dict(key=key, hash=digest, value=canonical(payload)),
                )
                .mappings()
                .first()
            )
            if row is None:
                row = (
                    conn.execute(
                        text("SELECT * FROM external_effects WHERE key=:key"),
                        dict(key=key),
                    )
                    .mappings()
                    .one()
                )
                if row["request_hash"] != digest:
                    raise IdempotencyConflict("Effect key has different payload")
            return row["value"]
