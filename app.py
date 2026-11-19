
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime
from src.alerts import send_alert
from src.realtime_simulator import generate_sensor_reading
from src.sensor_logger import save_sensor_reading
from streamlit import fragment

# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "failure_model.pkl"
DATA_PATH = BASE_DIR / "data" / "sensor_data.csv"

# Dashboard configuration
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Predictive Maintenance Dashboard")
st.caption("Industrial Equipment Monitoring System")

# Load machine learning model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# Sidebar
st.sidebar.header("Machine Controls")

machine_id = st.sidebar.selectbox(
    "Select Machine",
    ["MACHINE_001"]
)

st.sidebar.header("Sensor Readings")

temperature = st.sidebar.slider(
    "Temperature (°C)", 20, 130, 105
)

vibration = st.sidebar.slider(
    "Vibration", 0, 15, 12
)

pressure = st.sidebar.slider(
    "Pressure", 40, 180, 150
)

rpm = st.sidebar.slider(
    "RPM", 500, 2500, 2100
)

humidity = st.sidebar.slider(
    "Humidity (%)", 10, 95, 80
)

# Prepare sensor readings
sensor_data = pd.DataFrame([{
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "rpm": rpm,
    "humidity": humidity
}])

# Predict failure
probability = model.predict_proba(sensor_data)[0][1]
risk = probability * 100

# Machine overview
st.subheader("Machine Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Machine ID", machine_id)
col2.metric("Failure Probability", f"{risk:.1f}%")
col3.metric("Alert Threshold", "70%")

# Sensor metrics
st.subheader("Live Sensor Values")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Temperature", f"{temperature} °C")
c2.metric("Vibration", vibration)
c3.metric("Pressure", pressure)
c4.metric("RPM", rpm)
c5.metric("Humidity", f"{humidity}%")

# Automated Alert System
st.subheader("Maintenance Status")

# Prevent repeated emails during Streamlit reruns
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

if probability >= 0.70:

    st.error(
        f"🚨 HIGH FAILURE RISK! "
        f"Failure probability: {risk:.1f}%"
    )

    st.warning(
        "Recommended action: Inspect the machine immediately."
    )

    if not st.session_state.alert_sent:
        st.session_state.alert_sent = send_alert(
            probability, machine_id
    )

else:
    st.success(
        f"Machine operating normally. Risk: {risk:.1f}%"
    )

    st.session_state.alert_sent = False


# Probability visualization
st.subheader("Failure Probability")

st.progress(float(probability))

# Historical data
st.subheader("Historical Sensor Readings")

if DATA_PATH.exists():
    history = pd.read_csv(DATA_PATH)

    st.line_chart(
        history.tail(100).set_index("timestamp")[
            ["temperature", "vibration", "pressure"]
        ]
    )

    st.dataframe(history.tail(10), width="stretch")

st.caption(
    "Demonstration system using synthetic industrial sensor data."
)

st.caption(
    "Last dashboard update: " + datetime.now().strftime("%H:%M:%S")
)


# ----------------------------------------
# LIVE SENSOR MONITORING
# ----------------------------------------

st.divider()
st.header("Live Machine Sensor Monitoring")

st.info("Sensor readings automatically update every 5 seconds.")



@fragment(run_every="5s")
def live_monitor():

    # Initialize sensor history
    if "live_history" not in st.session_state:
        st.session_state.live_history = []

    # Generate new simulated reading
    reading = generate_sensor_reading()

    features = [
        "temperature",
        "vibration",
        "pressure",
        "rpm",
        "humidity"
    ]

    sensor_df = pd.DataFrame([{
        feature: reading[feature]
        for feature in features
    }])

    # Predict failure probability
    probability = float(
        model.predict_proba(sensor_df)[0][1]
    )

    reading["failure_probability"] = round(
        probability * 100, 2
    )
    # Save live sensor reading permanently
    save_sensor_reading(reading)

    # Save reading in session history
    st.session_state.live_history.append(reading)

    # Keep the latest 100 readings
    st.session_state.live_history = (
        st.session_state.live_history[-100:]
    )

    # Display current sensor readings
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Temperature",
            f"{reading['temperature']} °C"
        )
        st.metric(
            "Vibration",
            reading["vibration"]
        )

    with col2:
        st.metric(
            "Pressure",
            reading["pressure"]
        )
        st.metric(
            "RPM",
            reading["rpm"]
        )

    with col3:
        st.metric(
            "Humidity",
            reading["humidity"]
        )
        st.metric(
            "Failure Risk",
            f"{probability * 100:.1f}%"
        )

    st.caption(
        f"Last updated: {reading['timestamp']}"
    )

   
    # Automatic live email alerts
    if "live_alert_sent" not in st.session_state:
        st.session_state.live_alert_sent = False

        if probability >= 0.70:

            st.error(
                "HIGH FAILURE RISK! Maintenance required."
            )

    if not st.session_state.live_alert_sent:
        alert_success = send_alert(
            probability,
            machine_id
        )

        if alert_success:
            st.session_state.live_alert_sent = True
            st.success("Email alert sent successfully!")
        else:
            st.warning(
                "Email alert could not be sent. "
                "Check your email configuration."
            )

    else:
        st.success(
            "Machine operating normally."
        )

    # Reset alert status when risk becomes low
    st.session_state.live_alert_sent = False

    # Display real-time sensor history
    st.subheader("Real-Time Sensor History")

    history_df = pd.DataFrame(
        st.session_state.live_history
    )

    st.line_chart(
        history_df.set_index("timestamp")[
            ["temperature", "vibration",
             "pressure", "humidity"]
        ],
        width="stretch"
    )

    # Display latest readings in a table
    st.subheader("Recent Live Readings")

    st.dataframe(
        history_df.tail(10),
        width="stretch"
    )


live_monitor()
