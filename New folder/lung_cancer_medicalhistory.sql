
DROP TABLE IF EXISTS `medicalhistory`;

CREATE TABLE `medicalhistory` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `smoking_habit` tinyint(1) NOT NULL,
  `family_history` tinyint(1) NOT NULL,
  `symptoms` text NOT NULL,
  `previous_diseases` text,
  PRIMARY KEY (`history_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `medicalhistory_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `medicalhistory` WRITE;
UNLOCK TABLES;
