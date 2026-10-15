import logging

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.data.schemas.crop import CropCreate, CropUpdate
from app.services.crop_service import (
    create_crop_service,
    get_crop_service,
    get_crop_by_name_service,
    get_all_crops_service,
    update_crop_service,
    delete_crop_service,
)

crop_bp = Blueprint("crop", __name__, url_prefix="/api/crops")
logger = logging.getLogger(__name__)


def crop_to_dict(crop):
    return {
        "id": crop.id,
        "crop_name": crop.crop_name,
        "scientific_name": crop.scientific_name,
        "crop_type": crop.crop_type,
        "suitable_soil": crop.suitable_soil,
        "min_temperature": crop.min_temperature,
        "max_temperature": crop.max_temperature,
        "min_rainfall": crop.min_rainfall,
        "max_rainfall": crop.max_rainfall,
        "description": crop.description,
        "is_active": crop.is_active,
    }


@crop_bp.route("", methods=["POST"])
def create_crop_route():
    db = get_db_session()

    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        data = CropCreate.model_validate(payload)

        existing_crop = get_crop_by_name_service(db, data.crop_name)
        if existing_crop is not None:
            return jsonify({"error": "Crop name already exists"}), 409

        crop = create_crop_service(
            db=db,
            crop_name=data.crop_name,
            scientific_name=data.scientific_name,
            crop_type=data.crop_type,
            suitable_soil=data.suitable_soil,
            min_temperature=data.min_temperature,
            max_temperature=data.max_temperature,
            min_rainfall=data.min_rainfall,
            max_rainfall=data.max_rainfall,
            description=data.description,
        )

        return jsonify({
            "message": "Crop created successfully",
            "crop": crop_to_dict(crop),
        }), 201

    except ValidationError as error:
        return jsonify({
            "error": "Invalid crop data",
            "details": error.errors(include_input=False),
        }), 400
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Database constraint violation"}), 409
    except Exception:
        db.rollback()
        logger.exception("Failed to create crop")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@crop_bp.route("", methods=["GET"])
def get_all_crops_route():
    db = get_db_session()

    try:
        active_only = request.args.get("active_only", "true").lower()

        if active_only not in ("true", "false"):
            return jsonify({
                "error": "active_only must be true or false"
            }), 400

        crops = get_all_crops_service(
            db,
            active_only=(active_only == "true"),
        )

        return jsonify([crop_to_dict(crop) for crop in crops]), 200

    except Exception:
        logger.exception("Failed to retrieve crops")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@crop_bp.route("/<int:crop_id>", methods=["GET"])
def get_crop_route(crop_id):
    db = get_db_session()

    try:
        crop = get_crop_service(db, crop_id)

        if crop is None:
            return jsonify({"error": "Crop not found"}), 404

        return jsonify(crop_to_dict(crop)), 200

    except Exception:
        logger.exception("Failed to retrieve crop")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@crop_bp.route("/search", methods=["GET"])
def search_crop_route():
    db = get_db_session()

    try:
        crop_name = request.args.get("name", "").strip()

        if not crop_name:
            return jsonify({"error": "Provide a crop name using ?name="}), 400

        crop = get_crop_by_name_service(db, crop_name)

        if crop is None:
            return jsonify({"error": "Crop not found"}), 404

        return jsonify(crop_to_dict(crop)), 200

    except Exception:
        logger.exception("Failed to search for crop")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@crop_bp.route("/<int:crop_id>", methods=["PUT"])
def update_crop_route(crop_id):
    db = get_db_session()

    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict) or not payload:
            return jsonify({
                "error": "Request body must be a non-empty JSON object"
            }), 400

        data = CropUpdate.model_validate(payload)

        crop = update_crop_service(
            db=db,
            crop_id=crop_id,
            **data.model_dump(exclude_unset=True),
        )

        if crop is None:
            return jsonify({"error": "Crop not found"}), 404

        return jsonify({
            "message": "Crop updated successfully",
            "crop": crop_to_dict(crop),
        }), 200

    except ValidationError as error:
        return jsonify({
            "error": "Invalid crop data",
            "details": error.errors(include_input=False),
        }), 400
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Database constraint violation"}), 409
    except Exception:
        db.rollback()
        logger.exception("Failed to update crop")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@crop_bp.route("/<int:crop_id>", methods=["DELETE"])
def delete_crop_route(crop_id):
    db = get_db_session()

    try:
        deleted = delete_crop_service(db, crop_id)

        if not deleted:
            return jsonify({"error": "Crop not found"}), 404

        return jsonify({"message": "Crop deleted successfully"}), 200

    except Exception:
        db.rollback()
        logger.exception("Failed to delete crop")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()
