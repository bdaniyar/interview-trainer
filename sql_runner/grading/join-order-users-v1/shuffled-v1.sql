INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(81,'owner81@example.test',NULL,true,NULL,'2026-01-01'),
(9,'owner9@example.test','KZ',false,NULL,'2026-01-01'),
(300,'idle300@example.test','KZ',true,NULL,'2026-01-01'),
(4,'owner4@example.test',NULL,false,NULL,'2026-01-01'),
(42,'idle42@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(302,9,'paid','10.25','2026-03-01'),
(14,4,'new','11.25','2026-03-02'),
(77,81,'cancelled','12.25','2026-03-03'),
(8,9,'paid','13.25','2026-03-04'),
(901,81,'new','14.25','2026-03-05'),
(0,9,'cancelled','15.25','2026-03-06');
