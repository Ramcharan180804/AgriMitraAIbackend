from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.data.schemas.disease_detection import (
    DiseaseDetectionCreate,
    DiseaseDetectionResponse,
)
from app.services.disease_detection_service import (
    save_disease_detection,
    find_disease_detection,
    find_disease_detections_by_farm,
    find_all_disease_detections,
    remove_disease_detection,
)

disease_detection_bp = Blueprint(
    "disease_detection",
    __name__,
    url_prefix="/api/disease-detections",
)


def detection_to_dict(detection):
    return DiseaseDetectionResponse.model_validate(detection).model_dump(mode="json")


@disease_detection_bp.route("", methods=["POST"])
def create_disease_detection_route():
    try:
        data = DiseaseDetectionCreate.model_validate(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid request data",
            "details": error.errors(),
        }), 400

    db = get_db_session()
    try:
        detection = save_disease_detection(
            db=db,
            farm_id=data.farm_id,
            crop_id=data.crop_id,
            image_path=data.image_path,
            disease_name=data.disease_name,
            confidence_score=data.confidence_score,
            symptoms=data.symptoms,
            recommended_treatment=data.recommended_treatment,
        )
        return jsonify(detection_to_dict(detection)), 201
    except IntegrityError:
        db.rollback()
        return jsonify({
            "error": "Farm or crop ID does not exist"
        }), 400
    finally:
        db.close()


@disease_detection_bp.route("", methods=["GET"])
def get_all_disease_detections_route():
    try:
        limit = int(request.args.get("limit", 100))
        if not 1 <= limit <= 500:
            raise ValueError
    except ValueError:
        return jsonify({
            "error": "limit must be between 1 and 500"
        }), 400

    db = get_db_session()
    try:
        detections = find_all_disease_detections(db, limit)
        return jsonify([detection_to_dict(item) for item in detections]), 200
    finally:
        db.close()


@disease_detection_bp.route("/farm/<int:farm_id>", methods=["GET"])
def get_disease_detections_by_farm_route(farm_id):
    db = get_db_session()
    try:
        detections = find_disease_detections_by_farm(db, farm_id)
        return jsonify([detection_to_dict(item) for item in detections]), 200
    finally:
        db.close()


@disease_detection_bp.route("/<int:detection_id>", methods=["GET"])
def get_disease_detection_route(detection_id):
    db = get_db_session()
    try:
        detection = find_disease_detection(db, detection_id)
        if detection is None:
            return jsonify({"error": "Disease detection not found"}), 404

        return jsonify(detection_to_dict(detection)), 200
    finally:
        db.close()


@disease_detection_bp.route("/<int:detection_id>", methods=["DELETE"])
def delete_disease_detection_route(detection_id):
    db = get_db_session()
    try:
        detection = find_disease_detection(db, detection_id)
        if detection is None:
            return jsonify({"error": "Disease detection not found"}), 404

        remove_disease_detection(db, detection)
        return jsonify({
            "message": "Disease detection deleted successfully"
        }), 200
    finally:
        db.close()
