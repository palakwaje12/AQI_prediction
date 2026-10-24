# Air Quality Index (AQI) Prediction & Analysis

A machine learning application designed to analyze air quality trends and predict the Air Quality Index (AQI) across various Indian cities. This project evaluates linear regression, random forest, and XGBoost models to forecast AQI values.

---

## 📌 Project Overview

Air pollution is a critical environmental and public health issue. This project utilizes historical air quality data to build predictive models capable of estimating AQI based on key pollutant concentrations (such as $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{CO}$, $\text{SO}_2$, and $\text{O}_3$). 

### Key Features
* **Data Processing & Encoding:** Categorical city features are encoded using target encoding to optimize model training.
* **Model Training & Comparison:** Trained and evaluated multiple models:
  * Linear Regression
  * Random Forest
  * XGBoost Classifier/Regressor
* **Interactive Dashboard:** Backend setup prepared for integration with web/UI frontends (e.g., Streamlit/Flask).

---

## 📁 Repository Structure

```text
├── backend/
│   ├── app.py                          # Main application entry point
│   ├── hellostudent.java               # Sample Java utility file
│   └── models/
│       ├── aqi_xgboost_model.json      # Trained XGBoost model
│       ├── city_target_encoder.joblib  # Joblib-serialized city encoder
│       ├── city_target_encoder.pkl     # Pickle-serialized city encoder
│       ├── linear_regression_model.pkl # Trained Linear Regression model
│       └── random_forest_model.pkl     # Trained Random Forest model
└── README.md                           # Project documentation

📊 Models & Machine Learning Pipeline
Preprocessing: Feature scaling and city target encoding (city_target_encoder.pkl).

Model Training:

Linear Regression: Serves as the baseline model.

Random Forest: Handles non-linear feature relationships.

XGBoost: Provides optimized gradient boosting for enhanced prediction accuracy.

Model Persistence: Models are saved in .pkl and .json formats for fast inference during deployment.

🛠️ Installation & Setup
Prerequisites
Python 3.8 or higher

pip package installer

Steps
Clone the repository:

Bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
Navigate to the backend directory:

Bash
cd backend
Install dependencies:

Bash
pip install numpy pandas scikit-learn xgboost joblib flask
Run the application:

Bash
python app.py
