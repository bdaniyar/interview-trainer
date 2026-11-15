INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(31,'shuffled-owner31@example.test',NULL,true,NULL,'2026-01-01'),
(2,'shuffled-owner2@example.test','KZ',false,NULL,'2026-01-01');
INSERT INTO products (id,name,category,price) VALUES
(9007199254740993,'Fixture product 0','books','20.50'),
(8,'Fixture product 1','hardware','21.50'),
(51,'Fixture product 2','books','22.50'),
(0,'Fixture product 3','hardware','23.50');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(9007199254740995,31,'paid','10.25','2026-03-01'),
(19,2,'new','11.25','2026-03-02'),
(2,31,'cancelled','12.25','2026-03-03');
INSERT INTO order_items (order_id,product_id,quantity) VALUES
(9007199254740995,9007199254740993,2),
(2,8,1),
(19,9007199254740993,3),
(19,0,1);
