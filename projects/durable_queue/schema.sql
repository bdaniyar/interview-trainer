CREATE ROLE queueapp LOGIN PASSWORD 'synthetic-local-only' NOSUPERUSER NOCREATEDB NOCREATEROLE;
SELECT format('REVOKE ALL ON DATABASE %I FROM PUBLIC',current_database()) \gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO queueapp',current_database()) \gexec
REVOKE CONNECT,TEMPORARY ON DATABASE postgres,template1 FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
CREATE TABLE jobs (
 id uuid PRIMARY KEY, idempotency_key text NOT NULL UNIQUE, request_hash text NOT NULL,
 payload jsonb NOT NULL, state text NOT NULL DEFAULT 'queued'
 CHECK(state IN ('queued','running','succeeded','failed','cancelled')),
 attempts integer NOT NULL DEFAULT 0 CHECK(attempts>=0),
 max_attempts integer NOT NULL CHECK(max_attempts BETWEEN 1 AND 8),
 generation bigint NOT NULL DEFAULT 0 CHECK(generation>=0), worker_id text, lease_until timestamptz,
 available_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 created_at timestamptz NOT NULL DEFAULT clock_timestamp(), result jsonb,error text,
 CHECK((state='running' AND worker_id IS NOT NULL AND lease_until IS NOT NULL) OR
       (state<>'running' AND worker_id IS NULL AND lease_until IS NULL))
);
CREATE INDEX jobs_ready ON jobs(available_at,created_at,id) WHERE state IN ('queued','running');
CREATE TABLE effects(job_id uuid PRIMARY KEY REFERENCES jobs(id),value jsonb NOT NULL);
CREATE TABLE outbox(
 id uuid PRIMARY KEY,job_id uuid NOT NULL REFERENCES jobs(id),kind text NOT NULL,
 payload jsonb NOT NULL,created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 delivered boolean NOT NULL DEFAULT false, generation bigint NOT NULL DEFAULT 0,
 lease_until timestamptz, UNIQUE(job_id,kind)
);
CREATE TABLE external_effects(key text PRIMARY KEY,request_hash text NOT NULL,value jsonb NOT NULL);
GRANT USAGE ON SCHEMA public TO queueapp;
GRANT SELECT,INSERT,UPDATE,DELETE ON jobs,effects,outbox,external_effects TO queueapp;
ALTER ROLE queueapp SET statement_timeout='3000ms';
ALTER ROLE queueapp SET lock_timeout='2000ms';
ALTER ROLE queueapp SET idle_in_transaction_session_timeout='5000ms';
