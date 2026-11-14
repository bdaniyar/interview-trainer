INSERT INTO users VALUES
(40,'latest-tie-a@example.test','KZ',true,NULL,'2026-01-01'),
(70,'latest-tie-b@example.test','GE',true,NULL,'2026-01-02');
INSERT INTO orders VALUES
(21,40,'paid',10,'2026-09-03T00:00:00Z'),
(900,70,'paid',20,'2026-01-01T00:00:00Z'),
(11,40,'new',30,'2026-09-03T00:00:00Z'),
(12,70,'cancelled',40,'2026-09-03T00:00:00Z');
-- Deliberately legal date-only plan with the opposite ordering inside ties.
-- This is trusted bootstrap SQL, never a student capability or public index.
CREATE INDEX orders_adversarial_date_idx ON orders (created_at DESC, id ASC);
ANALYZE orders;
ALTER ROLE student SET enable_seqscan = off;
