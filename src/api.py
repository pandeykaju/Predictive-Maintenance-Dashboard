
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI(title="Predictive Maintenance API")

# Load trained machine learning model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "failure_model.pkl"

model = joblib.load(MODEL_PATH)

# Sensor input format
class SensorData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float
    humidity: float

# Home endpoint
@app.get("/")
def home():
    return {"message": "Predictive Maintenance API is running"}

# Prediction endpoint
@app.post("/predict")
def predict_failure(data: SensorData):

    sensor_df = pd.DataFrame([data.model_dump()])

    probability = float(model.predict_proba(sensor_df)[0][1])

    return {
        "failure_probability": round(probability * 100, 2),
        "risk_level": "HIGH" if probability >= 0.70 else "LOW",
        "maintenance_required": probability >= 0.70
    }