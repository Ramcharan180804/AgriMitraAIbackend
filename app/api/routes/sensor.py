import logging

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.data.schemas.sensor import SensorReadingCreate
from app.services.sensor_service import (
    create_sensor_reading_service,
    get_sensor_reading_service,
    get_sensor_readings_by_farm_service,
    get_latest_sensor_reading_service,
    get_all_sensor_readings_service,
    delete_sensor_reading_service,
)

sensor_bp = Blueprint("sensor", __name__, url_prefix="/api/sensors")
logger = logging.getLogger(__name__)


def sensor_to_dict(reading):
    return {
        "id": reading.id,
        "farm_id": reading.farm_id,
        "sensor_type": reading.sensor_type,
        "value": reading.value,
        "unit": reading.unit,
        "recorded_at": (
            reading.recorded_at.isoformat()
            if reading.recorded_at
            else None
        ),
    }


@sensor_bp.route("", methods=["POST"])
def create_sensor_reading_route():
    db = get_db_session()

    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        data = SensorReadingCreate.model_validate(payload)

        reading = create_sensor_reading_service(
            db=db,
            farm_id=data.farm_id,
            sensor_type=data.sensor_type,
            value=data.value,
            unit=data.unit,
            recorded_at=data.recorded_at,
        )

        return jsonify({
            "message": "Sensor reading created successfully",
            "reading": sensor_to_dict(reading),
        }), 201

    except ValidationError as error:
        return jsonify({
            "error": "Invalid sensor data",
            "details": error.errors(include_input=False),
        }), 400
    except IntegrityError:
        db.rollback()
        return jsonify({
            "error": "The specified farm_id does not exist or violates a database constraint"
        }), 400
    except Exception:
        db.rollback()
        logger.exception("Failed to create sensor reading")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@sensor_bp.route("", methods=["GET"])
def get_all_sensor_readings_route():
    db = get_db_session()

    try:
        raw_limit = request.args.get("limit", default="100")

        try:
            limit = int(raw_limit)
            if not 1 <= limit <= 500:
                raise ValueError
        except ValueError:
            return jsonify({
                "error": "limit must be an integer between 1 and 500"
            }), 400

        readings = get_all_sensor_readings_service(db, limit=limit)
        return jsonify([sensor_to_dict(item) for item in readings]), 200

    except Exception:
        logger.exception("Failed to retrieve sensor readings")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@sensor_bp.route("/<int:reading_id>", methods=["GET"])
def get_sensor_reading_route(reading_id):
    db = get_db_session()

    try:
        reading = get_sensor_reading_service(db, reading_id)

        if reading is None:
            return jsonify({"error": "Sensor reading not found"}), 404

        return jsonify(sensor_to_dict(reading)), 200

    except Exception:
        logger.exception("Failed to retrieve sensor reading")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@sensor_bp.route("/farm/<int:farm_id>", methods=["GET"])
def get_sensor_readings_by_farm_route(farm_id):
    db = get_db_session()

    try:
        raw_limit = request.args.get("limit", default="100")

        try:
            limit = int(raw_limit)
            if not 1 <= limit <= 500:
                raise ValueError
        except ValueError:
            return jsonify({
                "error": "limit must be an integer between 1 and 500"
            }), 400

        readings = get_sensor_readings_by_farm_service(
            db=db,
            farm_id=farm_id,
            limit=limit,
        )

        return jsonify([sensor_to_dict(item) for item in readings]), 200

    except Exception:
        logger.exception("Failed to retrieve farm sensor readings")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@sensor_bp.route("/farm/<int:farm_id>/latest/<string:sensor_type>", methods=["GET"])
def get_latest_sensor_reading_route(farm_id, sensor_type):
    db = get_db_session()

    try:
        reading = get_latest_sensor_reading_service(
            db=db,
            farm_id=farm_id,
            sensor_type=sensor_type,
        )

        if reading is None:
            return jsonify({"error": "No matching sensor reading found"}), 404

        return jsonify(sensor_to_dict(reading)), 200

    except Exception:
        logger.exception("Failed to retrieve latest sensor reading")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


@sensor_bp.route("/<int:reading_id>", methods=["DELETE"])
def delete_sensor_reading_route(reading_id):
    db = get_db_session()

    try:
        deleted = delete_sensor_reading_service(db, reading_id)

        if not deleted:
            return jsonify({"error": "Sensor reading not found"}), 404

        return jsonify({"message": "Sensor reading deleted successfully"}), 200

    except Exception:
        db.rollback()
        logger.exception("Failed to delete sensor reading")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()
