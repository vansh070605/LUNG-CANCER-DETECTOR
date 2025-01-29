from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lung_cancer.db'  # SQLite database in project directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    smoking = db.Column(db.String(20), nullable=False)
    symptoms = db.Column(db.String(200), nullable=False)
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
        age = request.form['age']
        smoking = request.form['smoking']
        symptoms = request.form['symptoms']
        
        # Replace with actual prediction logic
        result_message = f"No Lung Cancer detected for age {age}, smoking: {smoking}."

        # Save the result to the database
        prediction = Prediction(age=age, smoking=smoking, symptoms=symptoms, result=result_message)
        db.session.add(prediction)
        db.session.commit()

        # Render the result page with prediction details
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

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
