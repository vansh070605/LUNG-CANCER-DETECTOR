from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import joblib
import numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lung_cancer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

model = joblib.load('lung_cancer_model.pkl')

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    smoking = db.Column(db.String(20), nullable=False)
    symptoms = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', title="Home", year=datetime.now().year)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        smoking = 1 if request.form['smoking'].lower() == 'yes' else 0
        symptoms = 1 if request.form['symptoms'].lower() == 'yes' else 0

        user_input = np.array([[age, smoking, symptoms]])

        print(f"Input Data: {user_input}")

        prediction = model.predict(user_input)

        print(f"Raw Model Output: {prediction}")

        result_message = "Lung Cancer Detected 😔" if prediction[0] == 1 else "No Lung Cancer Detected ✅"

        prediction_entry = Prediction(age=age, smoking=str(smoking), symptoms=str(symptoms), result=result_message)
        db.session.add(prediction_entry)
        db.session.commit()

        return render_template('results.html', 
                               title="Result", 
                               result_message=result_message,
                               age=age,
                               smoking=smoking,
                               symptoms=symptoms,
                               year=datetime.now().year)

    return render_template('predict.html', title="Predict", year=datetime.now().year)


@app.route('/history')
def history():
    predictions = Prediction.query.order_by(Prediction.date.desc()).all()
    return render_template('history.html', title="History", predictions=predictions, year=datetime.now().year)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        db.session.query(Prediction).delete()
        db.session.commit()
        return redirect(url_for('history'))
    except:
        db.session.rollback()
        return "Error clearing history"

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
