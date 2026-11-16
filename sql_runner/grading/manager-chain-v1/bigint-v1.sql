-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(0,'0@phase8.test',NULL,true,NULL,'2026-01-01'),
(9007199254740993,'9007199254740993@phase8.test',NULL,true,0,'2026-01-01'),
(4,'4@phase8.test',NULL,true,9007199254740993,'2026-01-01');
