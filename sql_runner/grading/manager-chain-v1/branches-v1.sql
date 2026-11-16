-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(20,'20@phase8.test',NULL,true,NULL,'2026-01-01'),
(10,'10@phase8.test',NULL,true,20,'2026-01-01'),
(5,'5@phase8.test',NULL,true,10,'2026-01-01'),
(4,'4@phase8.test',NULL,true,10,'2026-01-01'),
(99,'99@phase8.test',NULL,true,NULL,'2026-01-01');
