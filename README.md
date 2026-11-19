# Predictive Maintenance Dashboard with Real-Time Alerts

## Project Overview

This project is a machine-learning-based predictive maintenance dashboard that monitors simulated industrial machine sensor data, estimates machine failure risk, and generates maintenance alerts.

The application includes an interactive Streamlit dashboard, a Random Forest classification model, a FastAPI prediction service, CSV-based sensor logging, Gmail email notifications, and Docker containerization.

## Objectives

- Monitor machine sensor readings.
- Estimate machine failure probability using machine learning.
- Display real-time sensor readings and risk indicators.
- Generate alerts when failure probability exceeds a defined threshold.
- Store sensor readings for historical monitoring.
- Deploy the dashboard and prediction API using Docker Compose.

## Technologies Used

- Python
- Streamlit
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Docker
- Docker Compose
- Gmail SMTP

## Machine Learning Model

**Algorithm:** Random Forest Classifier

**Input features:**
- Temperature
- Vibration
- Pressure
- RPM
- Humidity

**Output:**
- Failure probability
- Risk level
- Maintenance requirement

The model is trained on synthetic sensor data with simulated failure-risk labels. Predictions are demonstrations of the system's functionality, not validated real-world failure forecasts.

## Key Features

1. Interactive dashboard for monitoring machine conditions.
2. Automatic simulation of sensor readings.
3. Machine failure risk prediction.
4. Visualization of historical and live sensor readings.
5. High-risk maintenance notifications through Gmail.
6. CSV-based logging of sensor data.
7. REST API for predictions.
8. Docker Compose deployment of the dashboard and API.

## Project Structure

```text
real-time alert dashboard/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── data/
│   ├── sensor_data.csv
│   └── live_sensor_log.csv
├── models/
│   └── failure_model.pkl
└── src/
    ├── data_generator.py
    ├── train_model.py
    ├── predict.py
    ├── alerts.py
    ├── api.py
    ├── realtime_simulator.py
    └── sensor_logger.py
```

## How to Run

### Prerequisites

Install Docker Desktop and ensure the Docker Engine is running.

### Configure Email Alerts

Set the following environment variables in the PowerShell terminal:

- `ALERT_EMAIL`
- `ALERT_EMAIL_PASSWORD`
- `ALERT_RECEIVER`

Use a Gmail App Password for SMTP authentication. Never commit credentials to GitHub.

### Start the Application

```powershell
docker compose up -d --build
```

### Open the Applications

**Streamlit Dashboard:** http://localhost:8502

**FastAPI Documentation:** http://localhost:8001/docs

### Stop the Application

```powershell
docker compose down
```

## API Endpoint

**POST /predict**

Example request:

```json
{
  "temperature": 105,
  "vibration": 12,
  "pressure": 150,
  "rpm": 2100,
  "humidity": 80
}
```

Example response:

```json
{
  "failure_probability": 99,
  "risk_level": "HIGH",
  "maintenance_required": true
}
```

## Alert System

When the estimated failure probability reaches 70% or higher, the dashboard attempts to send an email notification to the configured receiver.

Email delivery requires valid SMTP credentials and an available internet connection.

## Testing

The project has been tested using:

- Docker container startup.
- Docker Compose service startup.
- FastAPI Swagger UI.
- HTTP 200 prediction responses.
- Streamlit dashboard startup.
- CSV sensor file access.

## Limitations

- Sensor readings are simulated rather than collected from physical industrial equipment.
- Training labels are synthetically generated.
- Model predictions have not been validated on real machine failures.
- Gmail alerts depend on external SMTP availability.

## Future Enhancements

- Integration with physical IoT sensors.
- Real industrial equipment datasets.
- Database storage.
- Multiple-machine monitoring.
- Model retraining and performance monitoring.
- SMS and mobile push notifications.

## Conclusion

This project demonstrates an end-to-end predictive maintenance prototype combining machine learning, simulated real-time monitoring, alert generation, REST APIs, and containerized deployment.