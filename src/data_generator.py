
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

NUM_RECORDS = 5000

# Generate sensor readings across a wider range
data = pd.DataFrame({
    "temperature": np.random.uniform(40, 120, NUM_RECORDS),
    "vibration": np.random.uniform(1, 14, NUM_RECORDS),
    "pressure": np.random.uniform(60, 160, NUM_RECORDS),
    "rpm": np.random.uniform(800, 2300, NUM_RECORDS),
    "humidity": np.random.uniform(20, 90, NUM_RECORDS)
})

# Calculate sensor risk score
risk = (
    (data["temperature"] > 95) * 0.30
    + (data["vibration"] > 9) * 0.30
    + (data["pressure"] > 135) * 0.15
    + (data["rpm"] > 1900) * 0.15
    + (data["humidity"] > 75) * 0.10
)

# Generate synthetic failure labels
noise = np.random.normal(0, 0.05, NUM_RECORDS)

data["failure_within_24h"] = (
    risk + noise > 0.35
).astype(int)

# Add timestamps
data.insert(
    0,
    "timestamp",
    pd.date_range(
        start="2026-01-01",
        periods=NUM_RECORDS,
        freq="h"
    )
)

data.insert(1, "machine_id", "MACHINE_001")

# Save dataset
output_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sensor_data.csv"
)

data.to_csv(output_path, index=False)

print("Improved dataset generated successfully!")
print("Total records:", len(data))
print("Failure records:", data["failure_within_24h"].sum())
print("Normal records:", (data["failure_within_24h"] == 0).sum())
print("\nDataset preview:")
print(data.head())
