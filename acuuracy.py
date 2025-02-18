import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

# Load the pre-trained model
model = pickle.load(open('models/model.pkl', 'rb'))

# Load the dataset
data = pd.read_csv('lung_cancer_examples.csv')

# Strip spaces from column names to handle extra spaces
data.columns = data.columns.str.strip()

# Verify the column names
print(data.columns)

# Preprocess the data
# Convert 'Smokes' to a binary feature (1 if Smokes > 0, else 0)
data['smoking'] = data['Smokes'].apply(lambda x: 1 if x > 0 else 0)

# Rename features to match the training dataset
data.rename(columns={'Age': 'age', 'Smokes': 'smoking'}, inplace=True)

# Add the missing features (make sure to fill them with appropriate values if they are necessary)
# Here, I'm assuming default values for 'gender', 'cough', 'chest_pain', 'fatigue', 'shortness_of_breath'.
# If you have real data for these, update them accordingly.
data['gender'] = 0  # Default or real value here
data['cough'] = 0   # Default or real value here
data['chest_pain'] = 0  # Default or real value here
data['fatigue'] = 0  # Default or real value here
data['shortness_of_breath'] = 0  # Default or real value here

# Prepare the input features for prediction
X = data[['age', 'gender', 'smoking', 'cough', 'chest_pain', 'fatigue', 'shortness_of_breath']]

# The target variable is 'Result'
y = data['Result']

# Make predictions
predictions = model.predict(X)

# Calculate accuracy
accuracy = accuracy_score(y, predictions)
print(f"Accuracy: {accuracy * 100:.2f}%")
