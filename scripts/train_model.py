import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Example dataset (replace this with your actual data)
data = pd.DataFrame({
    'age': [45, 60, 38, 55],
    'gender': [1, 0, 1, 0],  # Male = 1, Female = 0
    'smoking': [1, 0, 1, 1],  # Yes = 1, No = 0
    'cough': [1, 0, 1, 0],
    'chest_pain': [1, 1, 0, 0],
    'fatigue': [1, 0, 1, 0],
    'shortness_of_breath': [1, 0, 1, 0],
    'label': [1, 0, 1, 0]  # 1 = High risk, 0 = Low risk
})

X = data.drop('label', axis=1)
y = data['label']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
pickle.dump(model, open('models/model.pkl', 'wb'))