from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import pickle
from utils.prediction import predict_lung_cancer
from utils.pdf_generation import generate_pdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from io import BytesIO
import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER CHECK (age BETWEEN 0 AND 120),
        gender TEXT NOT NULL,  
        smoking TEXT CHECK (smoking IN ('yes', 'no')),
        cough TEXT CHECK (cough IN ('yes', 'no')),
        chest_pain TEXT CHECK (chest_pain IN ('yes', 'no')),
        fatigue TEXT CHECK (fatigue IN ('yes', 'no')),
        shortness_of_breath TEXT CHECK (shortness_of_breath IN ('yes', 'no')),
        prediction TEXT NOT NULL,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Table 'predictions' has been created successfully!")

app = Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', 'Female')  # Default: Female
        smoking = request.form.get('smoking', 'no').lower()
        cough = request.form.get('cough', 'no').lower()
        chest_pain = request.form.get('chest_pain', 'no').lower()
        fatigue = request.form.get('fatigue', 'no').lower()
        shortness_of_breath = request.form.get('shortness_of_breath', 'no').lower()

        if age is None or age <= 0:
            return "Invalid age value. Please enter a positive number.", 400

        gender = 1 if gender.lower() == 'male' else 0
        smoking = 1 if smoking == 'yes' else 0
        cough = 1 if cough == 'yes' else 0
        chest_pain = 1 if chest_pain == 'yes' else 0
        fatigue = 1 if fatigue == 'yes' else 0
        shortness_of_breath = 1 if shortness_of_breath == 'yes' else 0

        input_data = np.array([[age, gender, smoking, cough, chest_pain, fatigue, shortness_of_breath]])

        prediction = predict_lung_cancer(model, input_data)

        result = "High risk of lung cancer" if prediction == 1 else "Low risk of lung cancer"

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (age, gender, smoking, cough, chest_pain, fatigue, shortness_of_breath, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (age, 'Male' if gender else 'Female', 'yes' if smoking else 'no', 'yes' if cough else 'no', 
             'yes' if chest_pain else 'no', 'yes' if fatigue else 'no', 'yes' if shortness_of_breath else 'no', result)
        )
        conn.commit()
        conn.close()

        return render_template('result.html', result=result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500



@app.route('/predict_from_csv', methods=['POST'])
def predict_from_csv():
    try:
        dataset_path = 'lung_cancer_examples.csv'
        data = pd.read_csv(dataset_path)

        print(data.head())

        features = data[['Age', 'Smokes', 'AreaQ', 'Alkhol']].values

        predictions = model.predict(features)

        result = ['High risk of lung cancer' if pred == 1 else 'Low risk of lung cancer' for pred in predictions]

        data['Prediction'] = result

        return render_template('prediction_result.html', data=data.to_html())

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/generate_report', methods=['GET'])
def generate_report():
    return generate_pdf()


def generate_pdf():
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Lung Cancer Risk Report")
    c.drawString(100, 730, "Prediction: High risk (Example)")

    c.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="lung_cancer_report.pdf", mimetype="application/pdf")

def get_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT age, gender, smoking, cough, chest_pain, fatigue, shortness_of_breath, prediction FROM predictions")
    data = cursor.fetchall()
    conn.close()
    
    history_data = [
        {"age": row[0], "gender": row[1], "smoking": row[2], "cough": row[3], "chest_pain": row[4],
         "fatigue": row[5], "shortness_of_breath": row[6], "prediction": row[7]}
        for row in data
    ]
    return history_data

@app.route('/history')
def history():
    history_data = get_history()
    return render_template('history.html', history_data=history_data)


if __name__ == '__main__':
    app.run(debug=True)