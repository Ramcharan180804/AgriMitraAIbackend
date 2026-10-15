from flask import Flask, jsonify
from flask_cors import CORS

from app.api.routes.farmer import farmer_bp
from app.api.routes.farm import farm_bp
from app.api.routes.sensor import sensor_bp
from app.api.routes.crop import crop_bp
from app.api.routes.recommendation import recommendation_bp
from app.api.routes.disease_detection import disease_detection_bp
from app.api.routes.resource import resource_bp
from app.api.routes.booking import booking_bp
from app.api.routes.farming_activity import farming_activity_bp
from app.api.routes.evaluation import evaluation_bp

app = Flask(__name__)
CORS(app)

# Register all API blueprints
app.register_blueprint(farmer_bp)
app.register_blueprint(farm_bp)
app.register_blueprint(sensor_bp)
app.register_blueprint(crop_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(disease_detection_bp)
app.register_blueprint(resource_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(farming_activity_bp)
app.register_blueprint(evaluation_bp)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "Agri Mitra AI",
        "status": "running"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "service": "Agri Mitra AI"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
