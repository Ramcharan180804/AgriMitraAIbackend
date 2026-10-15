# Agri Mitra AI

AI service for the Agri Mitra agriculture application.

## Modules

### Module 1 - Crop Estimation

Estimates a suitable crop using:

- Temperature
- Humidity
- Soil Moisture
- pH
- Nitrogen
- Phosphorus
- Potassium

### Module 2 - Disease Detection

Detects crop diseases from images.

The image model will be trained and integrated later.

### Module 3 - Crop Prediction

Uses machine learning to predict suitable crops.

Technology:

- Python
- Pandas
- Scikit-learn
- Random Forest
- Joblib

### Module 4 - Node Connectivity

Processes sensor data received from:

ESP32 → Internet → Python/Spring Boot

## API

The Flask API runs on:

http://localhost:5000

## Run API

```bash
python api/app.py