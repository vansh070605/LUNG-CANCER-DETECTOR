import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# 📌 Save the trained model
joblib.dump(model, 'lung_cancer_model.pkl')

# 📌 Save label encoders for decoding later
joblib.dump(label_encoders, 'label_encoders.pkl')

print("✅ Model training complete! The trained model is saved as 'lung_cancer_model.pkl'.")
print("✅ Label encoders are saved as 'label_encoders.pkl'.")

# -------------- PREDICTION FUNCTION --------------
def predict_lung_cancer(user_input_dict):
    """
    Function to make predictions using the trained model.
    user_input_dict: Dictionary of input features with column names as keys.
    """
    # 📌 Load trained model & encoders
    model = joblib.load('lung_cancer_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')

    # 📌 Convert input dictionary to DataFrame
    user_input_df = pd.DataFrame([user_input_dict])  # Convert dict to DataFrame

    # 📌 Encode categorical inputs using the same encoders
    for column in user_input_df.columns:
        if column in label_encoders:  # Only encode if the column was categorical
            user_input_df[column] = label_encoders[column].transform(user_input_df[column])

    # 📌 Ensure column order matches training data
    user_input_df = user_input_df[X_train.columns]  # Keep only required columns

    # 📌 Make prediction
    prediction = model.predict(user_input_df)[0]

    # 📌 Decode the output (if necessary)
    result = "YES (High Risk)" if prediction == 1 else "NO (Low Risk)"
    
    return result

# -------------- EXAMPLE PREDICTION INPUT --------------
# Sample input with all 15 features
sample_input = {
    'AGE': 65,
    'GENDER': 'M',
    'SMOKING': 1,
    'YELLOW_FINGERS': 1,
    'ANXIETY': 0,
    'PEER_PRESSURE': 1,
    'CHRONIC DISEASE': 0,
    'FATIGUE ': 1,
    'ALLERGY ': 0,
    'WHEEZING': 1,
    'ALCOHOL CONSUMING': 1,
    'COUGHING': 1,
    'SHORTNESS OF BREATH': 1,
    'SWALLOWING DIFFICULTY': 0,
    'CHEST PAIN': 1
}

# 📌 Make a prediction using the trained model
prediction_result = predict_lung_cancer(sample_input)

print(f"📢 Predicted Lung Cancer Risk: {prediction_result}")
