# 🫁 Lung Cancer Detection  

## 📌 Project Overview  
**Lung Cancer Detector** is a **Flask-based web application** that predicts lung cancer risk based on user input (age, smoking history, symptoms) and **CT scan image analysis** for enhanced accuracy. The system provides a **user-friendly interface**, maintains prediction history, and allows users to download reports.  

## 🚀 Features  
✅ **Lung Cancer Risk Prediction** (Based on symptoms and medical history)  
✅ **CT Scan Image Analysis** (For enhanced accuracy)  
✅ **User-friendly Web Interface** (Built with Flask and HTML/CSS)  
✅ **Prediction History Tracking** (Stores user predictions in a database)  
✅ **Downloadable Reports** (Generate and download reports in PDF format)  
✅ **Admin Dashboard** (Manage user data and analyze trends)  

## 🛠️ Tech Stack  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Database:** SQLite  
- **Machine Learning Model:** Scikit-learn (RandomForestClassifier, joblib for model loading)  

## 📂 Project Structure
```
Lung_Cancer_Detection/
│── instance/                  # Database files
│   ├── lung_cancer.db         # SQLite database storing patient data
│   ├── lung_cancer.sql        # SQL schema for database setup
│── static/                     # Static files (CSS, JS, images)
│   ├── styles.css             # CSS for UI styling
│── templates/                  # HTML templates for frontend
│   ├── base.html              # Main layout file
│   ├── index.html             # Homepage
│   ├── home.html              # User dashboard
│   ├── about.html             # About the project
│   ├── predict.html           # Form for entering details
│   ├── results.html           # Displays prediction results
│   ├── history.html           # Shows past predictions
│── app.py                      # Main Flask application
│── train_model.py              # ML model training script
│── lung_cancer_model.pkl       # Trained machine learning model
│── label_encoders.pkl          # Encoded categorical features
│── survey_lung_cancer.csv      # Dataset for training the model
│── lung_cancer_er.jpg          # ER diagram for database
│── README.md                   # Project documentation
│── requirements.txt            # Required dependencies
```

## 🔧 Installation & Setup  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/vansh070605/LUNG-CANCER-DETECTOR.git
cd LUNG-CANCER-DETECTOR

### 2️⃣ Create a Virtual Environment  
```sh
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App  
```sh
python app.py
```
The application should now be running at **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**  

---

## 📷 Model Training (Optional)  
If you want to **train your own ML model**, use the following steps:  

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("survey_lung_cancer.csv")
X = df.drop("cancer", axis=1)
y = df["cancer"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "lung_cancer_model.pkl")
```

---

## 📊 Future Enhancements  
🔍 **Improve Model Accuracy** (Add more fields and deep learning support)  
📡 **Deploy Online** (Host on Vercel, AWS, or Render)  
📱 **Mobile-Friendly UI** (Enhance UX for mobile users)  
📊 **Data Visualization** (Add charts & graphs for better insights)  

---

## 📝 Contributors  
👨‍💻 **Vansh Agrawal** (Team Lead)  
👨‍💻 **Shashwat Sharma**  
👨‍💻 **Prajjwal Rawat**  
👨‍💻 **Abhyuday Singh Panwar**  
👨‍💻 **Harsh Khetan**  
