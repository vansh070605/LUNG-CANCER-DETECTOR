import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 📌 Load the dataset
df = pd.read_csv('survey lung cancer.csv')

# 📌 Fix column name inconsistencies by stripping spaces
df.columns = df.columns.str.strip()

# 📌 Check for missing values
df = df.dropna()  # Remove rows with missing values

# 📌 Encode categorical variables safely
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le  # Save encoders for later decoding

# 📌 Define features (X) and target (y)
X = df.drop(columns=['LUNG_CANCER'])  # Features
y = df['LUNG_CANCER']  # Target variable

# 📌 Ensure feature consistency by storing column order & dtypes
feature_order = X.columns.tolist()
feature_dtypes = X.dtypes.to_dict()

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

# 📌 Save feature order and dtypes
joblib.dump({'feature_order': feature_order, 'feature_dtypes': feature_dtypes}, 'feature_metadata.pkl')

print("✅ Model training complete! The trained model is saved as 'lung_cancer_model.pkl'.")
print("✅ Label encoders are saved as 'label_encoders.pkl'.")
print("✅ Feature metadata is saved as 'feature_metadata.pkl'.")

# -------------- PREDICTION FUNCTION --------------
def predict_lung_cancer(user_input_dict):
    # 📌 Load model and label encoders
    model = joblib.load('lung_cancer_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    metadata = joblib.load('feature_metadata.pkl')

    feature_order = metadata['feature_order']
    feature_dtypes = metadata['feature_dtypes']

    # 📌 Convert user input into DataFrame
    user_input_df = pd.DataFrame([user_input_dict])

    # 📌 Fix column inconsistencies
    user_input_df.columns = user_input_df.columns.str.strip()

    # 📌 Encode categorical inputs safely
    for column in user_input_df.columns:
        if column in label_encoders:
            if user_input_df[column].iloc[0] in label_encoders[column].classes_:
                user_input_df[column] = label_encoders[column].transform(user_input_df[column])
            else:
                print(f"⚠️ Warning: Unexpected category '{user_input_df[column].iloc[0]}' in column '{column}'. Using default encoding.")
                user_input_df[column] = label_encoders[column].transform([label_encoders[column].classes_[0]])[0]  # Use fallback

    # 📌 Ensure correct column order and fill missing columns
    user_input_df = user_input_df.reindex(columns=feature_order, fill_value=0)

    # 📌 Convert data types to match training set
    user_input_df = user_input_df.astype(feature_dtypes)

    # 📌 Debugging: Print processed input
    print("🔎 Processed Input Data:\n", user_input_df)

    # 📌 Make prediction
    prediction = model.predict(user_input_df)[0]
    probability = model.predict_proba(user_input_df)

    print("📊 Model Prediction Probabilities:", probability)
    print("🔢 Raw Prediction:", prediction)

    # Return a consistent result string
    return "High Risk" if prediction == 1 else "Low Risk"

# -------------- EXAMPLE PREDICTION INPUT --------------
sample_input = {
    'AGE': 65,
    'GENDER': 'M',
    'SMOKING': 1,
    'YELLOW_FINGERS': 1,
    'ANXIETY': 0,
    'PEER_PRESSURE': 1,
    'CHRONIC DISEASE': 0,
    'FATIGUE': 1,
    'ALLERGY': 0,
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
