INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(9007199254740993,'large-owner@example.test',NULL,true,NULL,'2026-01-01'),
(0,'zero-unused@example.test','KZ',false,NULL,'2026-01-01'),
(5,'other-unused@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(9007199254740995,9007199254740993,'paid','10.25','2026-03-01');
