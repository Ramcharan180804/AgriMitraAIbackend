def estimate_crop(temperature, humidity, soil_moisture,
                  ph, nitrogen, phosphorus, potassium):

    # Basic estimation logic.
    # This is a baseline rule-based estimator.
    # Later this can be replaced with a trained ML model.

    if 20 <= temperature <= 35 and 5.5 <= ph <= 7.5:
        if soil_moisture >= 60 and nitrogen >= 70:
            crop = "Rice"
        elif soil_moisture >= 40 and nitrogen >= 50:
            crop = "Maize"
        else:
            crop = "Millet"
    else:
        crop = "Millet"

    return crop


if __name__ == "__main__":

    result = estimate_crop(
        temperature=29,
        humidity=78,
        soil_moisture=65,
        ph=6.5,
        nitrogen=90,
        phosphorus=45,
        potassium=40
    )

    print("Estimated Crop:", result)