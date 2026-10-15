from pathlib import Path


def detect_disease(image_path):

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError("Image file not found")

    supported_formats = [".jpg", ".jpeg", ".png"]

    if path.suffix.lower() not in supported_formats:
        raise ValueError("Unsupported image format")

    # Actual CNN/image model will be connected here.
    # Currently returning model status.

    return {
        "disease": "MODEL_NOT_TRAINED",
        "confidence": 0.0,
        "suggestion": "Disease detection model is not trained yet."
    }


if __name__ == "__main__":

    print("Disease Detection Module")
    print("Image model is ready to be connected.")