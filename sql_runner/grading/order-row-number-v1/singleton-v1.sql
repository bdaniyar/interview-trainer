-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(4,'4@phase8.test',NULL,true,NULL,'2026-01-01'),
(91,'91@phase8.test','JP',false,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(51,4,'refunded',0.00,'2026-03-05');
