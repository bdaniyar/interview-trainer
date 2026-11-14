INSERT INTO users VALUES
(9007199254740993,'aggregate-0@example.test',NULL,true,NULL,'2026-01-01'),
(8,'aggregate-1@example.test','KZ',true,NULL,'2026-01-01'),
(41,'aggregate-2@example.test','KZ',true,NULL,'2026-01-01'),
(5,'aggregate-3@example.test',NULL,true,NULL,'2026-01-01'),
(96,'aggregate-4@example.test','KZ',true,NULL,'2026-01-01');
INSERT INTO orders VALUES
(70,41,'paid',10.25,'2026-03-01'),
(2,9007199254740993,'new',11.25,'2026-03-04'),
(91,8,'paid',12.25,'2026-03-07'),
(6,41,'new',13.25,'2026-03-10'),
(55,9007199254740993,'paid',14.25,'2026-03-13'),
(4,96,'cancelled',15.25,'2026-03-16'),
(23,8,'paid',16.25,'2026-03-19'),
(71,9007199254740993,'cancelled',17.25,'2026-03-22'),
(9,41,'paid',18.25,'2026-03-25'),
(3,9007199254740993,'paid',19.25,'2026-03-28');
