from module1_crop_estimation.prediction import estimate_crop


def crop_estimation_service(data):

    crop = estimate_crop(
        temperature=data["temperature"],
        humidity=data["humidity"],
        soil_moisture=data["soilMoisture"],
        ph=data["ph"],
        nitrogen=data["nitrogen"],
        phosphorus=data["phosphorus"],
        potassium=data["potassium"]
    )

    return {
        "module": "Crop Estimation",
        "estimatedCrop": crop
    }