from flask import Blueprint, request, jsonify, current_app as app
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.services.farmer_service import (
    create_farmer_service,
    get_farmer_service,
    get_all_farmers_service,
    update_farmer_service,
    delete_farmer_service,
)

farmer_bp = Blueprint("farmer", __name__)


def farmer_to_dict(farmer):
    return {
        "id": farmer.id,
        "name": farmer.name,
        "phone": farmer.phone,
        "village": farmer.village,
        "district": farmer.district,
    }


@farmer_bp.route("/farmers", methods=["POST"])
def add_farmer():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    phone = data.get("phone")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(phone, str) or not phone.strip():
        return jsonify({"error": "Phone is required"}), 400

    db = get_db_session()
    try:
        farmer = create_farmer_service(
            db,
            name.strip(),
            phone.strip(),
            data.get("village"),
            data.get("district"),
        )
        return jsonify({
            "message": "Farmer created successfully",
            "farmer": farmer_to_dict(farmer),
        }), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Phone number already exists"}), 409
    except Exception:
        db.rollback()
        app.logger.exception("Failed to create farmer")
        return jsonify({"error": "Failed to create farmer"}), 500
    finally:
        db.close()


@farmer_bp.route("/farmers", methods=["GET"])
def list_farmers():
    db = get_db_session()
    try:
        farmers = get_all_farmers_service(db)
        return jsonify([farmer_to_dict(f) for f in farmers]), 200
    except Exception:
        app.logger.exception("Failed to fetch farmers")
        return jsonify({"error": "Failed to fetch farmers"}), 500
    finally:
        db.close()


@farmer_bp.route("/farmers/<int:farmer_id>", methods=["GET"])
def get_farmer(farmer_id):
    db = get_db_session()
    try:
        farmer = get_farmer_service(db, farmer_id)
        if farmer is None:
            return jsonify({"error": "Farmer not found"}), 404
        return jsonify(farmer_to_dict(farmer)), 200
    except Exception:
        app.logger.exception("Failed to fetch farmer")
        return jsonify({"error": "Failed to fetch farmer"}), 500
    finally:
        db.close()


@farmer_bp.route("/farmers/<int:farmer_id>", methods=["PUT"])
def edit_farmer(farmer_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Provide farmer details to update"}), 400

    allowed = {"name", "phone", "village", "district"}
    if not set(data).issubset(allowed):
        return jsonify({"error": "Invalid field provided"}), 400

    for field in ("name", "phone"):
        if field in data and (
            not isinstance(data[field], str) or not data[field].strip()
        ):
            return jsonify({"error": f"{field} cannot be empty"}), 400

    db = get_db_session()
    try:
        farmer = update_farmer_service(
            db,
            farmer_id,
            name=data["name"].strip() if "name" in data else None,
            phone=data["phone"].strip() if "phone" in data else None,
            village=data.get("village"),
            district=data.get("district"),
        )

        if farmer is None:
            return jsonify({"error": "Farmer not found"}), 404

        return jsonify({
            "message": "Farmer updated successfully",
            "farmer": farmer_to_dict(farmer),
        }), 200
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Phone number already exists"}), 409
    except Exception:
        db.rollback()
        app.logger.exception("Failed to update farmer")
        return jsonify({"error": "Failed to update farmer"}), 500
    finally:
        db.close()


@farmer_bp.route("/farmers/<int:farmer_id>", methods=["DELETE"])
def remove_farmer(farmer_id):
    db = get_db_session()
    try:
        deleted = delete_farmer_service(db, farmer_id)

        if not deleted:
            return jsonify({"error": "Farmer not found"}), 404

        return jsonify({"message": "Farmer deleted successfully"}), 200
    except Exception:
        db.rollback()
        app.logger.exception("Failed to delete farmer")
        return jsonify({"error": "Failed to delete farmer"}), 500
    finally:
        db.close()
