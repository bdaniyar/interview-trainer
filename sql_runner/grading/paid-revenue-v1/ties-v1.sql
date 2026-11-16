-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(90,'90@phase8.test',NULL,true,NULL,'2026-01-01'),
(12,'12@phase8.test','DE',true,90,'2026-01-01'),
(4,'4@phase8.test','DE',false,12,'2026-01-01'),
(77,'77@phase8.test','US',true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(30,12,'paid',75.00,'2026-03-03'),
(2,12,'paid',75.00,'2026-03-03'),
(71,12,'new',400.00,'2026-03-01'),
(8,4,'cancelled',150.00,'2026-03-02'),
(19,4,'paid',149.99,'2026-03-02'),
(6,77,'paid',150.01,'2026-03-04');
