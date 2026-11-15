INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(40,'unused@example.test',NULL,true,NULL,'2026-01-01'),
(7,'repeat@example.test','KZ',false,NULL,'2026-01-01'),
(91,'other@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(501,7,'paid','10.25','2026-03-01'),
(18,91,'new','11.25','2026-03-02'),
(42,7,'cancelled','12.25','2026-03-03'),
(2,7,'paid','13.25','2026-03-04');
