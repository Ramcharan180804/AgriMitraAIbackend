from module3_crop_prediction.prediction.predict import predict_crop
from module3_crop_prediction.prediction.predict import predict_crop



def crop_prediction_service(data):

    crop = predict_crop(
        nitrogen=data["nitrogen"],
        phosphorus=data["phosphorus"],
        potassium=data["potassium"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        ph=data["ph"],
        rainfall=data["rainfall"]
    )

    return {
        "module": "Crop Prediction",
        "predictedCrop": crop
    }