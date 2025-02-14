# Lung Cancer Detection

## 📌 Project Overview
This is a **Lung Cancer Detector** web application built using **Flask**. The project allows users to enter medical details such as age, smoking history, and symptoms to predict the risk of lung cancer. Additionally, it supports **CT scan image analysis** to enhance prediction accuracy.

## 🚀 Features
- **User-friendly Web Interface** (Built with Flask and HTML/CSS)
- **Lung Cancer Risk Prediction** (Based on symptoms and medical history)
- **CT Scan Image Analysis** (For enhanced accuracy)
- **Prediction History Tracking** (Stores user predictions in a database)
- **Downloadable Reports** (Generate and download reports in PDF format)
- **Admin Dashboard** (Manage user data and analyze trends)

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Machine Learning Model:** Scikit-learn (joblib for model loading)

## 📂 Project Structure
```
Lung_Cancer_Detection/
│── static/            # CSS, JS, and image files
│── templates/         # HTML templates
│── lung_cancer_model.pkl   # Trained ML model
│── app.py            # Flask application
│── requirements.txt  # Required dependencies
│── README.md         # Project documentation
│── lung_cancer.db    # SQLite database
```

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vansh070605/LUNG-CANCER-DETECTOR.git
cd LUNG-CANCER-DETECTOR
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App
```bash
python app.py
```
The application should now be running at `http://127.0.0.1:5000/`

## 📷 Model Training (Optional)
If you want to train your own ML model, use the following steps:
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("lung_cancer_data.csv")
X = df.drop("cancer", axis=1)
y = df["cancer"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "lung_cancer_model.pkl")
```

## 📊 Future Enhancements
- 🔍 **Improve Model Accuracy** (Add more fields and deep learning support)
- 📡 **Deploy Online** (Host on Vercel or AWS)
- 📱 **Mobile-Friendly UI** (Enhance UX for mobile users)

## 📝 Contributors
- **Vansh Agrawal** (Team Lead)
- **Shashwat Sharma**
- **Prajjwal Rawat**
- **Abhyuday Singh Panwar**
- **Harsh Khetan**

## 📜 License
This project is licensed under the **MIT License**.

---
✨ *Feel free to contribute by submitting issues or pull requests!*

