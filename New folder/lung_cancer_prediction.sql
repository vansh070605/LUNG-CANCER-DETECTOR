

DROP TABLE IF EXISTS `prediction`;

CREATE TABLE `prediction` (
  `prediction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `prediction_result` varchar(50) NOT NULL,
  `confidence_score` float NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prediction_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `prediction_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `prediction` WRITE;

UNLOCK TABLES;

