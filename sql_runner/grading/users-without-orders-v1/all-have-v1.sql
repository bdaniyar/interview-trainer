INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(8,'has-eight@example.test',NULL,true,NULL,'2026-01-01'),
(19,'has-nineteen@example.test','KZ',false,NULL,'2026-01-01'),
(2,'has-two@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(8,19,'paid','10.25','2026-03-01'),
(19,2,'new','11.25','2026-03-02'),
(2,8,'cancelled','12.25','2026-03-03'),
(71,8,'paid','13.25','2026-03-04');
