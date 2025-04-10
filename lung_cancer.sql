-- 1️⃣ Create Database
CREATE DATABASE lung_cancer_db;
USE lung_cancer_db;

-- 2️⃣ Create Users Table (Authentication)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- 3️⃣ Create Predictions Table
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT CHECK (age BETWEEN 0 AND 120),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    smoking ENUM('yes', 'no') NOT NULL,
    cough ENUM('yes', 'no') NOT NULL,
    chest_pain ENUM('yes', 'no') NOT NULL,
    fatigue ENUM('yes', 'no') NOT NULL,
    shortness_of_breath ENUM('yes', 'no') NOT NULL,
    prediction VARCHAR(255) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4️⃣ Create User Predictions Table (Links Users & Predictions)
CREATE TABLE user_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    prediction_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE
);

-- 5️⃣ Insert Sample Data
INSERT INTO users (name, email, password_hash) 
VALUES ('John Doe', 'john@example.com', 'hashed_password');

INSERT INTO predictions (age, gender, smoking, cough, chest_pain, fatigue, shortness_of_breath, prediction)
VALUES (45, 'Male', 'yes', 'yes', 'no', 'yes', 'yes', 'High risk of lung cancer');

INSERT INTO user_predictions (user_id, prediction_id) 
VALUES (1, 1);

-- 6️⃣ Joins: Get All User Predictions
SELECT u.name, u.email, p.age, p.gender, p.smoking, p.prediction, p.prediction_date
FROM users u
JOIN user_predictions up ON u.id = up.user_id
JOIN predictions p ON up.prediction_id = p.id
ORDER BY p.prediction_date DESC;

-- 7️⃣ View: Active User Predictions
CREATE VIEW active_user_predictions AS
SELECT u.name, u.email, p.age, p.gender, p.smoking, p.prediction, p.prediction_date
FROM users u
JOIN user_predictions up ON u.id = up.user_id
JOIN predictions p ON up.prediction_id = p.id;

-- 8️⃣ Trigger: Log Deleted Predictions
CREATE TABLE deleted_predictions_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deleted_prediction_id INT,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_prediction_delete
AFTER DELETE ON predictions
FOR EACH ROW
BEGIN
    INSERT INTO deleted_predictions_log (deleted_prediction_id)
    VALUES (OLD.id);
END;
//
DELIMITER ;

-- 9️⃣ Cursor: Loop Through Predictions
DELIMITER //
CREATE PROCEDURE GetAllPredictions()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE pred_age INT;
    DECLARE pred_gender VARCHAR(10);
    DECLARE pred_risk VARCHAR(255);
    
    DECLARE cur CURSOR FOR SELECT age, gender, prediction FROM predictions;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO pred_age, pred_gender, pred_risk;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Printing in MySQL CLI
        SELECT CONCAT('Age: ', pred_age, ', Gender: ', pred_gender, ', Risk: ', pred_risk) AS Report;
    END LOOP;
    
    CLOSE cur;
END;
//
DELIMITER ;

-- 🔟 Report Queries:
-- 1️⃣ Count of Predictions Per Gender
SELECT gender, COUNT(*) AS total_predictions
FROM predictions
GROUP BY gender;

-- 2️⃣ Count of "High Risk" Predictions
SELECT COUNT(*) AS high_risk_count
FROM predictions
WHERE prediction = 'High risk of lung cancer';

-- 3️⃣ Latest Predictions in the Last 7 Days
SELECT * FROM predictions 
WHERE prediction_date >= NOW() - INTERVAL 7 DAY
ORDER BY prediction_date DESC;

-- 4️⃣ Find Users Who Made More Than 2 Predictions
SELECT u.name, u.email, COUNT(up.prediction_id) AS total_predictions
FROM users u
JOIN user_predictions up ON u.id = up.user_id
GROUP BY u.id
HAVING total_predictions > 2;

-- 5️⃣ Find Users Who Haven't Made a Prediction
SELECT u.name, u.email FROM users u
LEFT JOIN user_predictions up ON u.id = up.user_id
WHERE up.user_id IS NULL;
