from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.data.models.recommendation import Recommendation
from app.data.schemas.recommendation import (
    RecommendationCreate,
    RecommendationResponse,
)
from app.services.recommendation_service import (
    save_recommendation,
    find_recommendation,
    find_recommendations_by_farm,
    find_all_recommendations,
    remove_recommendation,
)

recommendation_bp = Blueprint(
    "recommendations", __name__, url_prefix="/api/recommendations"
)


def recommendation_to_dict(recommendation):
    return RecommendationResponse.model_validate(recommendation).model_dump(mode="json")


@recommendation_bp.route("", methods=["POST"])
def create_recommendation_route():
    try:
        data = RecommendationCreate.model_validate(request.get_json(silent=True) or {})
    except ValidationError as error:
        return jsonify({"error": "Invalid request data", "details": error.errors()}), 400

    db = get_db_session()
    try:
        recommendation = save_recommendation(
            db=db,
            farm_id=data.farm_id,
            crop_id=data.crop_id,
            confidence_score=data.confidence_score,
            recommendation_reason=data.recommendation_reason,
            season=data.season,
        )
        return jsonify(recommendation_to_dict(recommendation)), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Farm or crop ID does not exist"}), 400
    finally:
        db.close()


@recommendation_bp.route("", methods=["GET"])
def get_all_recommendations_route():
    try:
        limit = int(request.args.get("limit", 100))
        if not 1 <= limit <= 500:
            raise ValueError
    except ValueError:
        return jsonify({"error": "limit must be between 1 and 500"}), 400

    db = get_db_session()
    try:
        recommendations = find_all_recommendations(db, limit)
        return jsonify([recommendation_to_dict(item) for item in recommendations]), 200
    finally:
        db.close()


@recommendation_bp.route("/farm/<int:farm_id>", methods=["GET"])
def get_recommendations_by_farm_route(farm_id):
    db = get_db_session()
    try:
        recommendations = find_recommendations_by_farm(db, farm_id)
        return jsonify([recommendation_to_dict(item) for item in recommendations]), 200
    finally:
        db.close()


@recommendation_bp.route("/<int:recommendation_id>", methods=["GET"])
def get_recommendation_route(recommendation_id):
    db = get_db_session()
    try:
        recommendation = find_recommendation(db, recommendation_id)
        if recommendation is None:
            return jsonify({"error": "Recommendation not found"}), 404
        return jsonify(recommendation_to_dict(recommendation)), 200
    finally:
        db.close()


@recommendation_bp.route("/<int:recommendation_id>", methods=["DELETE"])
def delete_recommendation_route(recommendation_id):
    db = get_db_session()
    try:
        recommendation = find_recommendation(db, recommendation_id)
        if recommendation is None:
            return jsonify({"error": "Recommendation not found"}), 404

        remove_recommendation(db, recommendation)
        return jsonify({"message": "Recommendation deleted successfully"}), 200
    finally:
        db.close()
