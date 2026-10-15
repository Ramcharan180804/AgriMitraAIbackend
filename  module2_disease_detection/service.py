from module2_disease_detection.prediction import detect_disease


def disease_detection_service(image_path):

    result = detect_disease(image_path)

    return {
        "module": "Disease Detection",
        "result": result
    }