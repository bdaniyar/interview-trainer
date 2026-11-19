CREATE TABLE inventory(id bigint PRIMARY KEY,available integer NOT NULL CHECK(available>=0));
INSERT INTO inventory VALUES(1,1),(2,2);
CREATE TABLE bookings(
 id uuid PRIMARY KEY, request_key text UNIQUE NOT NULL, request_hash text NOT NULL,
 room_id bigint NOT NULL REFERENCES inventory(id),created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE outbox(
 id uuid PRIMARY KEY,payload jsonb NOT NULL,state text NOT NULL DEFAULT 'pending'
 CHECK(state IN ('pending','sending','delivered','failed')),
 generation bigint NOT NULL DEFAULT 0,attempts integer NOT NULL DEFAULT 0 CHECK(attempts BETWEEN 0 AND 5),
 lease_until timestamptz,available_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 CHECK((state='sending')=(lease_until IS NOT NULL))
);
CREATE INDEX outbox_ready ON outbox(available_at,id) WHERE state IN ('pending','sending');
