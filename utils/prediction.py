import numpy as np

def predict_lung_cancer(model, input_data):
    # Get prediction probabilities (if available)
    prob = model.predict_proba(input_data)
    print(f"Prediction probabilities: {prob}")  # Log the probabilities

    # Assuming class 1 (high risk) is at index 1 and using a threshold of 0.5
    return 1 if prob[0][1] > 0.5 else 0  # Classify as high risk if probability > 0.5
