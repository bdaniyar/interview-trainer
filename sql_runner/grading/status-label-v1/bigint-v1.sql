-- Synthetic trusted fixture; all FK relationships remain valid.
INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(0,'0@phase8.test','JP',true,NULL,'2026-01-01'),
(9007199254740993,'9007199254740993@phase8.test','US',false,0,'2026-01-01'),
(4,'4@phase8.test','US',true,9007199254740993,'2026-01-01'),
(19,'19@phase8.test',NULL,true,NULL,'2026-01-01');
INSERT INTO orders (id,user_id,status,total,created_at) VALUES
(9007199254740995,9007199254740993,'paid',20.25,'2026-03-04'),
(0,4,'paid',200.00,'2026-03-01'),
(57,9007199254740993,'paid',180.00,'2026-03-01'),
(8,4,'new',20.25,'2026-03-03'),
(3,19,'queued',0.00,'2026-03-02');
