
import joblib
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "failure_model.pkl"

# Load trained model
model = joblib.load(MODEL_PATH)

# Sample live machine sensor readings
sensor_data = pd.DataFrame([{
    "temperature": 105,
    "vibration": 12,
    "pressure": 150,
    "rpm": 2100,
    "humidity": 80
}])

# Predict failure probability
probability = model.predict_proba(sensor_data)[0][1]

# Display prediction
print("\nPREDICTIVE MAINTENANCE RESULT")
print("--------------------------------")
print("Temperature:", sensor_data["temperature"].iloc[0])
print("Vibration:", sensor_data["vibration"].iloc[0])
print("Pressure:", sensor_data["pressure"].iloc[0])
print("RPM:", sensor_data["rpm"].iloc[0])
print("Humidity:", sensor_data["humidity"].iloc[0])

print("\nFailure Probability:", round(probability * 100, 2), "%")

if probability >= 0.70:
    print("ALERT: HIGH FAILURE RISK!")
else:
    print("STATUS: Machine operating normally.")
