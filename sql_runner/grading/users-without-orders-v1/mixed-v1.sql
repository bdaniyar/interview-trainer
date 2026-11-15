INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(47,'mixed-47@example.test',NULL,true,NULL,'2026-01-01'),
(0,'mixed-zero@example.test','KZ',false,NULL,'2026-01-01'),
(8,'mixed-8@example.test','KZ',true,NULL,'2026-01-01'),
(901,'mixed-idle@example.test',NULL,false,NULL,'2026-01-01'),
(9007199254740993,'mixed-big@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(72,47,'paid','10.25','2026-03-01'),
(5,8,'new','11.25','2026-03-02'),
(91,47,'cancelled','12.25','2026-03-03');
