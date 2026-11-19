
import random
from datetime import datetime

def generate_sensor_reading(machine_id="MACHINE_001"):
    """
    Generate simulated live sensor readings
    for a machine.
    """

    # Occasionally generate abnormal readings
    high_risk = random.random() < 0.20

    if high_risk:
        temperature = random.uniform(95, 120)
        vibration = random.uniform(10, 15)
        pressure = random.uniform(130, 180)
        rpm = random.uniform(1800, 2500)
        humidity = random.uniform(70, 95)
    else:
        temperature = random.uniform(40, 75)
        vibration = random.uniform(1, 5)
        pressure = random.uniform(60, 110)
        rpm = random.uniform(900, 1600)
        humidity = random.uniform(30, 65)

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "machine_id": machine_id,
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 2),
        "pressure": round(pressure, 2),
        "rpm": round(rpm, 2),
        "humidity": round(humidity, 2),
    }

if __name__ == "__main__":
    reading = generate_sensor_reading()
    print("Live Sensor Reading:")
    print(reading)