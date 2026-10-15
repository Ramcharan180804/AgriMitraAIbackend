from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
import logging

from app.data.database.connection import get_db_session
from app.data.schemas.farm import FarmCreate, FarmUpdate
from app.services.farm_service import (
    create_farm_service,
    get_farm_service,
    get_farms_by_farmer_service,
    get_all_farms_service,
    update_farm_service,
    delete_farm_service,
)

farm_bp = Blueprint("farm", __name__, url_prefix="/api/farms")
logger = logging.getLogger(__name__)


def farm_to_dict(farm):
    return {
        "id": farm.id,
        "farm_name": farm.farm_name,
        "area_acres": farm.area_acres,
        "farmer_id": farm.farmer_id,
        "location": farm.location,
        "district": farm.district,
        "village": farm.village,
    }


@farm_bp.route("", methods=["POST"])
def create_farm_route():
    db = get_db_session()

    try:
        data = FarmCreate.model_validate(request.get_json(silent=True) or {})

        farm = create_farm_service(
            db=db,
            farm_name=data.farm_name,
            area_acres=data.area_acres,
            farmer_id=data.farmer_id,
            location=data.location,
            district=data.district,
            village=data.village,
        )

        return jsonify({
            "message": "Farm created successfully",
            "farm": farm_to_dict(farm),
        }), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except IntegrityError:
        db.rollback()
        return jsonify({
            "error": "Invalid farmer_id or database constraint violation"
        }), 400
    except Exception:
        db.rollback()
        logger.exception("Failed to create farm")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@farm_bp.route("", methods=["GET"])
def get_all_farms_route():
    db = get_db_session()

    try:
        farms = get_all_farms_service(db)
        return jsonify([farm_to_dict(farm) for farm in farms]), 200
    except Exception:
        logger.exception("Failed to retrieve farms")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@farm_bp.route("/<int:farm_id>", methods=["GET"])
def get_farm_route(farm_id):
    db = get_db_session()

    try:
        farm = get_farm_service(db, farm_id)

        if farm is None:
            return jsonify({"error": "Farm not found"}), 404

        return jsonify(farm_to_dict(farm)), 200
    except Exception:
        logger.exception("Failed to retrieve farm")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@farm_bp.route("/farmer/<int:farmer_id>", methods=["GET"])
def get_farms_by_farmer_route(farmer_id):
    db = get_db_session()

    try:
        farms = get_farms_by_farmer_service(db, farmer_id)
        return jsonify([farm_to_dict(farm) for farm in farms]), 200
    except Exception:
        logger.exception("Failed to retrieve farmer farms")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@farm_bp.route("/<int:farm_id>", methods=["PUT"])
def update_farm_route(farm_id):
    db = get_db_session()

    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        data = FarmUpdate.model_validate(payload)

        farm = update_farm_service(
            db=db,
            farm_id=farm_id,
            farm_name=data.farm_name,
            area_acres=data.area_acres,
            location=data.location,
            district=data.district,
            village=data.village,
        )

        if farm is None:
            return jsonify({"error": "Farm not found"}), 404

        return jsonify({
            "message": "Farm updated successfully",
            "farm": farm_to_dict(farm),
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.rollback()
        logger.exception("Failed to update farm")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@farm_bp.route("/<int:farm_id>", methods=["DELETE"])
def delete_farm_route(farm_id):
    db = get_db_session()

    try:
        deleted = delete_farm_service(db, farm_id)

        if not deleted:
            return jsonify({"error": "Farm not found"}), 404

        return jsonify({"message": "Farm deleted successfully"}), 200
    except Exception:
        db.rollback()
        logger.exception("Failed to delete farm")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()
