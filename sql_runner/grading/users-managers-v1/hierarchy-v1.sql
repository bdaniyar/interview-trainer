INSERT INTO users (id,email,country,active,manager_id,created_at) VALUES
(80,'z-root@example.test',NULL,true,NULL,'2026-01-01'),
(0,'root-zero@example.test','KZ',false,NULL,'2026-01-01'),
(17,'mid@example.test','KZ',true,80,'2026-01-01'),
(300,'late-employee@example.test',NULL,false,17,'2026-01-01'),
(9,'early-employee@example.test','KZ',true,17,'2026-01-01'),
(450,'other-employee@example.test','KZ',false,80,'2026-01-01');
