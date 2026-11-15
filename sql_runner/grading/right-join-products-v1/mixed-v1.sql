INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(41,'product-owner41@example.test',NULL,true,NULL,'2026-01-01'),
(9,'product-owner9@example.test','KZ',false,NULL,'2026-01-01');
INSERT INTO products (id,name,category,price) VALUES
(700,'Fixture product 0','books','20.50'),
(0,'Fixture product 1','hardware','21.50'),
(401,'Fixture product 2','books','22.50'),
(9007199254740993,'Fixture product 3','hardware','23.50');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(91,41,'paid','10.25','2026-03-01'),
(2,9,'new','11.25','2026-03-02'),
(14,41,'cancelled','12.25','2026-03-03'),
(0,9,'paid','13.25','2026-03-04');
INSERT INTO order_items (order_id,product_id,quantity) VALUES
(91,700,2),
(2,700,1),
(2,0,3),
(14,700,1);
