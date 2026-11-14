INSERT INTO users VALUES
(81,'aggregate-0@example.test',NULL,true,NULL,'2026-01-01'),
(9,'aggregate-1@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders VALUES
(47,81,'paid',10.25,'2026-03-01'),
(2,9,'new',11.25,'2026-03-04'),
(90,81,'cancelled',12.25,'2026-03-07'),
(21,9,'paid',13.25,'2026-03-10'),
(6,81,'new',14.25,'2026-03-13'),
(300,81,'paid',15.25,'2026-03-16');
