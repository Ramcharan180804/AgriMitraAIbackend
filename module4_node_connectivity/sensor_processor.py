from datetime import datetime


REQUIRED_FIELDS = [
    "temperature",
    "humidity",
    "soilMoisture",
    "ph",
    "nitrogen",
    "phosphorus",
    "potassium"
]


def process_sensor_data(data):

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in data
    ]

    if missing_fields:
        raise ValueError(
            f"Missing sensor fields: {missing_fields}"
        )

    processed_data = {
        "temperature": float(data["temperature"]),
        "humidity": float(data["humidity"]),
        "soilMoisture": float(data["soilMoisture"]),
        "ph": float(data["ph"]),
        "nitrogen": float(data["nitrogen"]),
        "phosphorus": float(data["phosphorus"]),
        "potassium": float(data["potassium"]),
        "receivedAt": datetime.now().isoformat()
    }

    return processed_data


if __name__ == "__main__":

    sensor_data = {
        "temperature": 29,
        "humidity": 78,
        "soilMoisture": 65,
        "ph": 6.5,
        "nitrogen": 90,
        "phosphorus": 45,
        "potassium": 40
    }

    result = process_sensor_data(sensor_data)

    print(result)