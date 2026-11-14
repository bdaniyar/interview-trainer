INSERT INTO users VALUES
(40,'latest-instants-a@example.test','KZ',true,NULL,'2026-01-01'),
(70,'latest-instants-b@example.test','GE',true,NULL,'2026-01-02');
INSERT INTO orders VALUES
(700,40,'paid',1,'2026-10-01T05:00:00.123455+05:00'),
(9,70,'new',2,'2026-10-01T00:00:00.123456Z'),
(41,40,'paid',3,'2026-10-01T05:00:00.123456+05:00'),
(1000,70,'paid',4,'2026-01-01T00:00:00Z');
