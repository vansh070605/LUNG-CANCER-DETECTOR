-- Create the Database
CREATE DATABASE lung_cancer;
USE lung_cancer;

-- User Table (Patients)
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    contact VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Medical History Table
CREATE TABLE MedicalHistory (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    smoking_habit BOOLEAN NOT NULL,
    family_history BOOLEAN NOT NULL,
    symptoms TEXT NOT NULL,
    previous_diseases TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Test Results Table
CREATE TABLE TestResult (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    ct_scan_result TEXT NOT NULL,
    biopsy_result TEXT NOT NULL,
    x_ray_result TEXT NOT NULL,
    test_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Prediction Table
CREATE TABLE Prediction (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    prediction_result VARCHAR(50) NOT NULL,
    confidence_score FLOAT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Report Table
CREATE TABLE Report (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    report_pdf VARCHAR(255) NOT NULL,
    generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);
