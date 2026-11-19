CREATE ROLE ordersapp LOGIN PASSWORD 'synthetic-orders-only' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE notifyapp LOGIN PASSWORD 'synthetic-notify-only' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE monoapp LOGIN PASSWORD 'synthetic-mono-only' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE arch_orders;
CREATE DATABASE arch_notify;
CREATE DATABASE arch_mono;
REVOKE CONNECT,TEMPORARY ON DATABASE postgres,template1 FROM PUBLIC;
REVOKE ALL ON DATABASE arch_orders,arch_notify,arch_mono FROM PUBLIC;
GRANT CONNECT ON DATABASE arch_orders TO ordersapp;
GRANT CONNECT ON DATABASE arch_notify TO notifyapp;
GRANT CONNECT ON DATABASE arch_mono TO monoapp;
\connect arch_orders
REVOKE ALL ON SCHEMA public FROM PUBLIC;
\i /init/orders.sql
GRANT USAGE ON SCHEMA public TO ordersapp;
GRANT SELECT,INSERT,UPDATE ON ALL TABLES IN SCHEMA public TO ordersapp;
\connect arch_notify
REVOKE ALL ON SCHEMA public FROM PUBLIC;
\i /init/notifications.sql
GRANT USAGE ON SCHEMA public TO notifyapp;
GRANT SELECT,INSERT ON ALL TABLES IN SCHEMA public TO notifyapp;
\connect arch_mono
REVOKE ALL ON SCHEMA public FROM PUBLIC;
\i /init/orders.sql
\i /init/notifications.sql
GRANT USAGE ON SCHEMA public TO monoapp;
GRANT SELECT,INSERT,UPDATE ON ALL TABLES IN SCHEMA public TO monoapp;
ALTER ROLE ordersapp SET statement_timeout='3s';
ALTER ROLE ordersapp SET lock_timeout='2s';
ALTER ROLE ordersapp SET idle_in_transaction_session_timeout='5s';
ALTER ROLE notifyapp SET statement_timeout='3s';
ALTER ROLE notifyapp SET lock_timeout='2s';
ALTER ROLE notifyapp SET idle_in_transaction_session_timeout='5s';
ALTER ROLE monoapp SET statement_timeout='3s';
ALTER ROLE monoapp SET lock_timeout='2s';
ALTER ROLE monoapp SET idle_in_transaction_session_timeout='5s';
