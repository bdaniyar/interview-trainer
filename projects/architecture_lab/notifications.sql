CREATE TABLE inbox(event_id uuid PRIMARY KEY,request_hash text NOT NULL,payload jsonb NOT NULL);
CREATE TABLE notifications(
 order_id uuid PRIMARY KEY,event_id uuid NOT NULL UNIQUE REFERENCES inbox(event_id),
 kind text NOT NULL,correlation_id text NOT NULL,created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
