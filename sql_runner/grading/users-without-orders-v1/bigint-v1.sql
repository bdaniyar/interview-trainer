INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(9007199254740993,'idle-huge@example.test',NULL,true,NULL,'2026-01-01'),
(2,'ordered-two@example.test','KZ',false,NULL,'2026-01-01'),
(43,'ordered-forty@example.test','KZ',true,NULL,'2026-01-01'),
(0,'idle-zero@example.test',NULL,false,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(11,2,'paid','10.25','2026-03-01'),
(91,43,'new','11.25','2026-03-02'),
(3,2,'cancelled','12.25','2026-03-03');
