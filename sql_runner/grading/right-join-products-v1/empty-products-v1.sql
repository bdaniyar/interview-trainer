INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(10,'empty-products-owner@example.test',NULL,true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(40,10,'paid','10.25','2026-03-01');
