from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "crop_model.pkl"

def predict_crop(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall
):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Crop model not found. Train the model first."
        )

    model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame([{
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    prediction = model.predict(input_data)[0]

    return prediction


if __name__ == "__main__":

    crop = predict_crop(
        nitrogen=90,
        phosphorus=45,
        potassium=40,
        temperature=29,
        humidity=78,
        ph=6.5,
        rainfall=200
    )

    print("Predicted Crop:", crop)