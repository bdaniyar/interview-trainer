INSERT INTO users VALUES
(81,'aggregate-0@example.test',NULL,true,NULL,'2026-01-01'),
(9,'aggregate-1@example.test','KZ',true,NULL,'2026-01-01'),
(40,'aggregate-2@example.test','KZ',true,NULL,'2026-01-01'),
(2,'aggregate-3@example.test',NULL,true,NULL,'2026-01-01');
INSERT INTO orders VALUES
(91,9,'paid',10.25,'2026-03-01'),
(2,81,'new',11.25,'2026-03-04'),
(300,9,'cancelled',12.25,'2026-03-07'),
(7,40,'paid',13.25,'2026-03-10'),
(44,81,'cancelled',14.25,'2026-03-13'),
(6,9,'new',15.25,'2026-03-16');
