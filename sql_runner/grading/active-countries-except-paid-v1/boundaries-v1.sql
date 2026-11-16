-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(22,'22@phase8.test','DE',true,NULL,'2026-01-01'),
(7,'7@phase8.test','DE',true,22,'2026-01-01'),
(4,'4@phase8.test',NULL,true,7,'2026-01-01'),
(88,'88@phase8.test',NULL,false,NULL,'2026-01-01'),
(13,'13@phase8.test','US',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(99,22,'paid',149.99,'2026-03-01'),
(10,7,'paid',100.00,'2026-03-02'),
(11,7,'paid',50.00,'2026-03-03'),
(50,4,'paid',150.01,'2026-03-04'),
(51,4,'cancelled',900.00,'2026-03-04'),
(52,88,'new',-10.00,'2026-03-05'),
(54,13,'paid',50.00,'2026-03-02'),
(53,13,'paid',50.00,'2026-03-02');
