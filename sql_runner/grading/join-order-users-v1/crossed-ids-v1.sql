INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(2,'owner-two@example.test',NULL,true,NULL,'2026-01-01'),
(17,'owner-seventeen@example.test','KZ',false,NULL,'2026-01-01'),
(99,'owner-ninety@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(99,17,'paid','10.25','2026-03-01'),
(2,99,'new','11.25','2026-03-02'),
(17,2,'cancelled','12.25','2026-03-03'),
(250,17,'paid','13.25','2026-03-04');
