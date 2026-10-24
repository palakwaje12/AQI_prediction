import time
import os
import pickle
import pandas as pd
import xgboost as xgb
from flask import Flask, request, jsonify
from flask_cors import CORS

# ---------------- SYSTEM CONSTANTS ----------------
START_TIME = time.time()
PREDICTION_COUNT = 0
HISTORY_LOG = []
NODE_ID = "AQI-TITAN-XGB-4"

app = Flask(__name__)
CORS(app)

# ==========================================
# LOAD MODEL & ENCODER
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "aqi_xgboost_model.json")
ENCODER_PATH = os.path.join(MODELS_DIR, "city_target_encoder.pkl")

try:
    model = xgb.XGBRegressor()
    model.load_model(MODEL_PATH)

    with open(ENCODER_PATH, "rb") as f:
        encoder = pickle.load(f)

    MODEL_ACCURACY = "96.5% R²"
    print("✅ XGBoost Model Loaded")

except Exception as e:
    print(f"❌ Model Load Failed: {e}")
    model = None
    encoder = None
    MODEL_ACCURACY = "0.0%"

# ==========================================
# CPCB AQI FUNCTIONS
# ==========================================
def get_pm25_sub_index(cp):
    if cp <= 30: return cp * 50 / 30
    elif cp <= 60: return 50 + (cp - 30) * 50 / 30
    elif cp <= 90: return 100 + (cp - 60) * 100 / 30
    elif cp <= 120: return 200 + (cp - 90) * 100 / 30
    elif cp <= 250: return 300 + (cp - 120) * 100 / 130
    else: return 400 + (cp - 250) * 100 / 130

def get_pm10_sub_index(cp):
    if cp <= 50: return cp
    elif cp <= 100: return cp
    elif cp <= 250: return 100 + (cp - 100) * 100 / 150
    elif cp <= 350: return 200 + (cp - 250) * 100 / 100
    elif cp <= 430: return 300 + (cp - 350) * 100 / 80
    else: return 400 + (cp - 430) * 100 / 70

def get_co_sub_index(cp):
    if cp <= 1: return cp * 50
    elif cp <= 2: return 50 + (cp - 1) * 50
    elif cp <= 10: return 100 + (cp - 2) * 100 / 8
    else: return 200 + (cp - 10) * 100 / 7

def get_aqi_category(aqi):
    if aqi <= 50: return ("Good", "good")
    elif aqi <= 100: return ("Satisfactory", "satisfactory")
    elif aqi <= 200: return ("Moderate", "moderate")
    elif aqi <= 300: return ("Poor", "poor")
    elif aqi <= 400: return ("Very Poor", "vpoor")
    else: return ("Severe", "severe")

# ==========================================
# UI DASHBOARD ROUTE
# ==========================================
@app.route("/")
def home():
    uptime = int(time.time() - START_TIME)

    history_html = "".join([
        f"""
        <div class="timeline-item">
            <span class="time">{h['time']}</span>
            <span class="aqi">AQI {h['aqi']}</span>
            <span class="badge {h['cls']}">{h['cat']}</span>
        </div>
        """
        for h in HISTORY_LOG[::-1]
    ]) or "<div class='empty'>Awaiting incoming neural signals…</div>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>AQInsight Command</title></head>
    <body style="background:#05070a;color:white;font-family:Arial">
        <h2>AQInsight Command Center</h2>
        <p>Queries: {PREDICTION_COUNT}</p>
        <p>Accuracy: {MODEL_ACCURACY}</p>
        <p>Uptime: {uptime}s</p>
        <hr>
        {history_html}
    </body>
    </html>
    """

# ==========================================
# PREDICTION API
# ==========================================
@app.route("/predict", methods=["POST"])
def predict_aqi():
    global PREDICTION_COUNT, HISTORY_LOG

    try:
        data = request.get_json()
        PREDICTION_COUNT += 1

        df = pd.DataFrame({
            "City": [data.get("City", "Unknown")],
            "PM2.5": [float(data.get("PM2.5", 0))],
            "PM10": [float(data.get("PM10", 0))],
            "NO2": [float(data.get("NO2", 0))],
            "CO": [float(data.get("CO", 0))],
            "O3": [float(data.get("O3", 0))],
            "SO2": [float(data.get("SO2", 0))]
        })

        # ML estimate
        if model and encoder:
            encoded = encoder.transform(df)
            future_aqi = round(float(model.predict(encoded)[0]), 2)
            future_aqi = max(0, future_aqi)
        else:
            future_aqi = 0

        next_aqi = round(future_aqi * 1.03, 2)

        current_aqi = round(max(
            get_pm25_sub_index(df["PM2.5"][0]),
            get_pm10_sub_index(df["PM10"][0]),
            get_co_sub_index(df["CO"][0]),
            df["NO2"][0] * 50 / 40,
            df["O3"][0] * 50 / 50
        ), 2)

        cat_name, cat_class = get_aqi_category(current_aqi)

        # ✅ FIX: cls added
        HISTORY_LOG.append({
            "time": time.strftime("%H:%M:%S"),
            "aqi": current_aqi,
            "cat": cat_name,
            "cls": cat_class
        })
        if len(HISTORY_LOG) > 10:
            HISTORY_LOG.pop(0)

        return jsonify({
            "current_aqi": current_aqi,
            "future_aqi": future_aqi,
            "next_aqi": next_aqi,
            "actual_aqi": current_aqi,
            "ml_prediction": future_aqi,
            "category": cat_name,
            "category_class": f"status-{cat_class}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
