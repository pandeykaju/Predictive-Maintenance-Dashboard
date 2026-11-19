
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / "data" / "live_sensor_log.csv"

FIELDS = [
    "timestamp",
    "machine_id",
    "temperature",
    "vibration",
    "pressure",
    "rpm",
    "humidity",
    "failure_probability"
]

def save_sensor_reading(reading):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = (
        LOG_PATH.exists()
        and LOG_PATH.stat().st_size > 0
    )

    with open(
        LOG_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            field: reading[field]
            for field in FIELDS
        })