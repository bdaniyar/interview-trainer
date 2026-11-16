-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(1,'1@phase8.test',NULL,true,NULL,'2026-01-01'),
(9007199254740993,'9007199254740993@phase8.test',NULL,true,1,'2026-01-01'),
(7,'7@phase8.test',NULL,true,9007199254740993,'2026-01-01'),
(99,'99@phase8.test',NULL,true,7,'2026-01-01'),
(4,'4@phase8.test',NULL,true,99,'2026-01-01'),
(32,'32@phase8.test',NULL,true,NULL,'2026-01-01');
