BEGIN TRANSACTION;
CREATE TABLE predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        smoking TEXT,
        cough TEXT,
        chest_pain TEXT,
        fatigue TEXT,
        shortness_of_breath TEXT,
        prediction TEXT
    );
INSERT INTO "predictions" VALUES(1,19,'Male','yes','no','yes','yes','no','High risk of lung cancer');
INSERT INTO "predictions" VALUES(2,100,'Male','yes','yes','yes','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(3,19,'Male','no','no','no','no','no','Low risk of lung cancer');
INSERT INTO "predictions" VALUES(4,75,'Male','yes','no','no','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(5,24,'Male','no','no','no','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(6,52,'Male','yes','no','no','no','yes','Low risk of lung cancer');
INSERT INTO "predictions" VALUES(7,76,'Female','yes','yes','yes','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(8,56,'Female','no','no','no','no','yes','Low risk of lung cancer');
INSERT INTO "predictions" VALUES(9,54,'Male','no','yes','yes','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(10,69,'Male','yes','yes','yes','yes','yes','High risk of lung cancer');
INSERT INTO "predictions" VALUES(11,20,'Male','yes','no','yes','no','yes','Low risk of lung cancer');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('predictions',11);
COMMIT;
