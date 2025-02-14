from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lung_cancer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load the trained ML model
model = joblib.load('lung_cancer_model.pkl')  # Ensure this file exists

# Database Model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    smoking = db.Column(db.String(10), nullable=False)
    yellow_fingers = db.Column(db.String(10), nullable=False)
    anxiety = db.Column(db.String(10), nullable=False)
    peer_pressure = db.Column(db.String(10), nullable=False)
    chronic_disease = db.Column(db.String(10), nullable=False)
    fatigue = db.Column(db.String(10), nullable=False)
    allergy = db.Column(db.String(10), nullable=False)
    wheezing = db.Column(db.String(10), nullable=False)
    alcohol = db.Column(db.String(10), nullable=False)
    coughing = db.Column(db.String(10), nullable=False)
    shortness_of_breath = db.Column(db.String(10), nullable=False)
    swallowing_difficulty = db.Column(db.String(10), nullable=False)
    chest_pain = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.id}>'

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', title="Home", year=datetime.now().year)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get input values from the form
        age = int(request.form['age'])
        gender = 1 if request.form['gender'] == 'Male' else 0
        smoking = 1 if request.form['smoking'] == 'Yes' else 0
        yellow_fingers = 1 if request.form['yellow_fingers'] == 'Yes' else 0
        anxiety = 1 if request.form['anxiety'] == 'Yes' else 0
        peer_pressure = 1 if request.form['peer_pressure'] == 'Yes' else 0
        chronic_disease = 1 if request.form['chronic_disease'] == 'Yes' else 0
        fatigue = 1 if request.form['fatigue'] == 'Yes' else 0
        allergy = 1 if request.form['allergy'] == 'Yes' else 0
        wheezing = 1 if request.form['wheezing'] == 'Yes' else 0
        alcohol = 1 if request.form['alcohol'] == 'Yes' else 0
        coughing = 1 if request.form['coughing'] == 'Yes' else 0
        shortness_of_breath = 1 if request.form['shortness_of_breath'] == 'Yes' else 0
        swallowing_difficulty = 1 if request.form['swallowing_difficulty'] == 'Yes' else 0
        chest_pain = 1 if request.form['chest_pain'] == 'Yes' else 0

        # Convert input to model format
        user_input = np.array([[age, gender, smoking, yellow_fingers, anxiety, peer_pressure,
                                chronic_disease, fatigue, allergy, wheezing, alcohol, coughing,
                                shortness_of_breath, swallowing_difficulty, chest_pain]])

        # Get prediction from ML model
        prediction = model.predict(user_input)

        # Interpret prediction result
        result_message = "Lung Cancer Detected 😔" if prediction[0] == 1 else "No Lung Cancer Detected ✅"

        # Save the prediction result to the database
        prediction_entry = Prediction(
            age=age,
            gender="Male" if gender == 1 else "Female",
            smoking="Yes" if smoking == 1 else "No",
            yellow_fingers="Yes" if yellow_fingers == 1 else "No",
            anxiety="Yes" if anxiety == 1 else "No",
            peer_pressure="Yes" if peer_pressure == 1 else "No",
            chronic_disease="Yes" if chronic_disease == 1 else "No",
            fatigue="Yes" if fatigue == 1 else "No",
            allergy="Yes" if allergy == 1 else "No",
            wheezing="Yes" if wheezing == 1 else "No",
            alcohol="Yes" if alcohol == 1 else "No",
            coughing="Yes" if coughing == 1 else "No",
            shortness_of_breath="Yes" if shortness_of_breath == 1 else "No",
            swallowing_difficulty="Yes" if swallowing_difficulty == 1 else "No",
            chest_pain="Yes" if chest_pain == 1 else "No",
            result=result_message
        )
        db.session.add(prediction_entry)
        db.session.commit()

        return render_template('results.html', 
                               title="Result", 
                               result_message=result_message,
                               age=age,
                               gender="Male" if gender == 1 else "Female",
                               smoking="Yes" if smoking == 1 else "No",
                               yellow_fingers="Yes" if yellow_fingers == 1 else "No",
                               anxiety="Yes" if anxiety == 1 else "No",
                               peer_pressure="Yes" if peer_pressure == 1 else "No",
                               chronic_disease="Yes" if chronic_disease == 1 else "No",
                               fatigue="Yes" if fatigue == 1 else "No",
                               allergy="Yes" if allergy == 1 else "No",
                               wheezing="Yes" if wheezing == 1 else "No",
                               alcohol="Yes" if alcohol == 1 else "No",
                               coughing="Yes" if coughing == 1 else "No",
                               shortness_of_breath="Yes" if shortness_of_breath == 1 else "No",
                               swallowing_difficulty="Yes" if swallowing_difficulty == 1 else "No",
                               chest_pain="Yes" if chest_pain == 1 else "No",
                               year=datetime.now().year)

    return render_template('predict.html', title="Predict", year=datetime.now().year)

@app.route('/history')
def history():
    predictions = Prediction.query.order_by(Prediction.date.desc()).all()
    return render_template('history.html', title="History", predictions=predictions, year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    db.session.query(Prediction).delete()
    db.session.commit()
    return render_template('history.html', title="History", predictions=[], year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)
