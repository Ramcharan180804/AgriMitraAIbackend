from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.data.database.connection import get_db_session
from app.data.schemas.farming_activity import (
    FarmingActivityCreate,
    FarmingActivityUpdate,
    FarmingActivityResponse,
)
from app.services.farming_activity_service import (
    add_farming_activity,
    find_farming_activity,
    find_farming_activities_by_farm,
    find_all_farming_activities,
    edit_farming_activity,
    remove_farming_activity,
)

farming_activity_bp = Blueprint(
    "farming_activity",
    __name__,
    url_prefix="/api/farming-activities",
)


def activity_to_dict(activity):
    return FarmingActivityResponse.model_validate(activity).model_dump(mode="json")


@farming_activity_bp.route("", methods=["POST"])
def create_activity():
    db = get_db_session()
    try:
        data = FarmingActivityCreate.model_validate(request.get_json(silent=True) or {})

        activity = add_farming_activity(
            db=db,
            farm_id=data.farm_id,
            activity_type=data.activity_type,
            description=data.description,
            resource_used=data.resource_used,
            quantity_used=data.quantity_used,
            cost=data.cost,
            notes=data.notes,
        )

        return jsonify(activity_to_dict(activity)), 201

    except ValidationError as error:
        db.rollback()
        return jsonify({"error": "Validation failed", "details": error.errors(include_url=False)}), 400
    except ValueError as error:
        db.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.rollback()
        return jsonify({"error": "Could not create farming activity"}), 500
    finally:
        db.close()


@farming_activity_bp.route("", methods=["GET"])
def get_activities():
    db = get_db_session()
    try:
        limit = request.args.get("limit", default=100, type=int)
        activities = find_all_farming_activities(db, limit)

        return jsonify([activity_to_dict(item) for item in activities]), 200
    finally:
        db.close()


@farming_activity_bp.route("/farm/<int:farm_id>", methods=["GET"])
def get_activities_by_farm(farm_id):
    db = get_db_session()
    try:
        activities = find_farming_activities_by_farm(db, farm_id)
        return jsonify([activity_to_dict(item) for item in activities]), 200
    finally:
        db.close()


@farming_activity_bp.route("/<int:activity_id>", methods=["GET"])
def get_activity(activity_id):
    db = get_db_session()
    try:
        activity = find_farming_activity(db, activity_id)

        if activity is None:
            return jsonify({"error": "Farming activity not found"}), 404

        return jsonify(activity_to_dict(activity)), 200
    finally:
        db.close()


@farming_activity_bp.route("/<int:activity_id>", methods=["PUT"])
def update_activity(activity_id):
    db = get_db_session()
    try:
        data = FarmingActivityUpdate.model_validate(
            request.get_json(silent=True) or {}
        )
        updates = data.model_dump(exclude_unset=True)

        if not updates:
            return jsonify({"error": "Provide at least one field to update"}), 400

        activity = edit_farming_activity(db, activity_id, updates)

        if activity is None:
            return jsonify({"error": "Farming activity not found"}), 404

        return jsonify(activity_to_dict(activity)), 200

    except ValidationError as error:
        db.rollback()
        return jsonify({"error": "Validation failed", "details": error.errors(include_url=False)}), 400
    except ValueError as error:
        db.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.rollback()
        return jsonify({"error": "Could not update farming activity"}), 500
    finally:
        db.close()


@farming_activity_bp.route("/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    db = get_db_session()
    try:
        deleted = remove_farming_activity(db, activity_id)

        if not deleted:
            return jsonify({"error": "Farming activity not found"}), 404

        return jsonify({"message": "Farming activity deleted successfully"}), 200
    finally:
        db.close()
