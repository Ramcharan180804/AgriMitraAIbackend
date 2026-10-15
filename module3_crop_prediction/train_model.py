from pathlib import Path

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "crop_model.pkl"

def train_model():

    print("Loading dataset...")

    data = pd.read_csv(DATASET_PATH)

    features = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    X = data[features]
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training model...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("Model training completed.")
    print("Accuracy:", accuracy)
    print("Model saved:", MODEL_PATH)


if __name__ == "__main__":
    train_model()