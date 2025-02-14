import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # You can change this model
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 📌 Load the dataset
df = pd.read_csv('survey lung cancer.csv')

# 📌 Check for missing values
df = df.dropna()  # Remove rows with missing values

# 📌 Encode categorical variables
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le  # Save encoders for later decoding

# 📌 Define features (X) and target (y)
X = df.drop(columns=['LUNG_CANCER'])  # Features
y = df['LUNG_CANCER']  # Target variable

# 📌 Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 📌 Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📌 Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 📌 Save the trained model
joblib.dump(model, 'lung_cancer_model.pkl')

# 📌 Save label encoders for decoding later
joblib.dump(label_encoders, 'label_encoders.pkl')

print("✅ Model training complete! The trained model is saved as 'lung_cancer_model.pkl'.")
