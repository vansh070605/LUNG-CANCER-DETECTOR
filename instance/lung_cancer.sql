CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'doctor', 'user')) DEFAULT 'user'
);

CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    age INTEGER NOT NULL,
    smoking INTEGER NOT NULL,
    yellow_fingers INTEGER NOT NULL,
    anxiety INTEGER NOT NULL,
    peer_pressure INTEGER NOT NULL,
    chronic_disease INTEGER NOT NULL,
    fatigue INTEGER NOT NULL,
    allergy INTEGER NOT NULL,
    wheezing INTEGER NOT NULL,
    alcohol_consumption INTEGER NOT NULL,
    coughing INTEGER NOT NULL,
    shortness_of_breath INTEGER NOT NULL,
    swallowing_difficulty INTEGER NOT NULL,
    chest_pain INTEGER NOT NULL,
    lung_cancer_prediction TEXT CHECK(lung_cancer_prediction IN ('Yes', 'No')) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
