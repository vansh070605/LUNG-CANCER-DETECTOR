from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import pickle
from utils.prediction import predict_lung_cancer
from utils.pdf_generation import generate_pdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from io import BytesIO
import pandas as pd

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
        smoking = request.form.get('smoking', 'no').lower()    # Default: no
        cough = request.form.get('cough', 'no').lower()        # Default: no
        chest_pain = request.form.get('chest_pain', 'no').lower()  # Default: no
        fatigue = request.form.get('fatigue', 'no').lower()        # Default: no
        shortness_of_breath = request.form.get('shortness_of_breath', 'no').lower()  # Default: no

        print(f"Received: Age={age}, Gender={gender}, Smoking={smoking}, Cough={cough}, Chest Pain={chest_pain}, Fatigue={fatigue}, Shortness of Breath={shortness_of_breath}")

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

        return render_template('result.html', result=result)

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return f"Error: {str(e)}", 500  # Catch any unexpected errors



@app.route('/predict_from_csv', methods=['POST'])
def predict_from_csv():
    try:
        dataset_path = 'lung_cancer_examples.csv'  # Ensure correct path
        data = pd.read_csv(dataset_path)

        print(data.head())

        features = data[['Age', 'Smokes', 'AreaQ', 'Alkhol']].values

        predictions = model.predict(features)

        result = ['High risk of lung cancer' if pred == 1 else 'Low risk of lung cancer' for pred in predictions]

        data['Prediction'] = result

        return render_template('prediction_result.html', data=data.to_html())

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return f"Error: {str(e)}", 500  # Catch any unexpected errors


@app.route('/generate_report', methods=['GET'])
def generate_report():
    return generate_pdf()  # This will handle PDF creation and returning it as a response


def generate_pdf():
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Lung Cancer Risk Report")
    c.drawString(100, 730, "Prediction: High risk (Example)")  # You can replace this with actual prediction results

    c.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="lung_cancer_report.pdf", mimetype="application/pdf")


if __name__ == '__main__':
    app.run(debug=True)
