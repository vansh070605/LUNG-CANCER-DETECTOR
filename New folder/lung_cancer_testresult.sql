

DROP TABLE IF EXISTS `testresult`;

CREATE TABLE `testresult` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `ct_scan_result` text NOT NULL,
  `biopsy_result` text NOT NULL,
  `x_ray_result` text NOT NULL,
  `test_date` date NOT NULL,
  PRIMARY KEY (`test_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `testresult_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `testresult` WRITE;

UNLOCK TABLES;

