

DROP TABLE IF EXISTS `report`;

CREATE TABLE `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `report_pdf` varchar(255) NOT NULL,
  `generated_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `report` WRITE;

UNLOCK TABLES;

