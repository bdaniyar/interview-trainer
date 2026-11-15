INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(8,'single-item-owner@example.test',NULL,true,NULL,'2026-01-01');
INSERT INTO products (id,name,category,price) VALUES
(13,'Fixture product 0','books','20.50'),
(99,'Fixture product 1','hardware','21.50');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(0,8,'paid','10.25','2026-03-01');
INSERT INTO order_items (order_id,product_id,quantity) VALUES
(0,99,1);
