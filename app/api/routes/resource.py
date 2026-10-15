from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.data.database.connection import get_db_session
from app.data.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)
from app.services.resource_service import (
    save_resource,
    find_resource,
    find_all_resources,
    find_resources_by_type,
    edit_resource,
    remove_resource,
)

resource_bp = Blueprint(
    "resources", __name__, url_prefix="/api/resources"
)


def resource_to_dict(resource):
    return ResourceResponse.model_validate(resource).model_dump(mode="json")


@resource_bp.route("", methods=["POST"])
def create_resource_route():
    try:
        data = ResourceCreate.model_validate(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid request data",
            "details": error.errors(),
        }), 400

    db = get_db_session()
    try:
        resource = save_resource(
            db=db,
            **data.model_dump(),
        )
        return jsonify(resource_to_dict(resource)), 201
    finally:
        db.close()


@resource_bp.route("", methods=["GET"])
def get_all_resources_route():
    try:
        limit = int(request.args.get("limit", 100))
        if not 1 <= limit <= 500:
            raise ValueError
    except ValueError:
        return jsonify({
            "error": "limit must be between 1 and 500"
        }), 400

    available_only = request.args.get(
        "available_only", "false"
    ).lower() == "true"

    db = get_db_session()
    try:
        resources = find_all_resources(
            db,
            available_only=available_only,
            limit=limit,
        )
        return jsonify([resource_to_dict(item) for item in resources]), 200
    finally:
        db.close()


@resource_bp.route("/search", methods=["GET"])
def search_resources_route():
    resource_type = request.args.get("type", "").strip()
    if not resource_type:
        return jsonify({
            "error": "Provide a resource type using ?type=..."
        }), 400

    db = get_db_session()
    try:
        resources = find_resources_by_type(db, resource_type)
        return jsonify([resource_to_dict(item) for item in resources]), 200
    finally:
        db.close()


@resource_bp.route("/<int:resource_id>", methods=["GET"])
def get_resource_route(resource_id):
    db = get_db_session()
    try:
        resource = find_resource(db, resource_id)
        if resource is None:
            return jsonify({"error": "Resource not found"}), 404

        return jsonify(resource_to_dict(resource)), 200
    finally:
        db.close()


@resource_bp.route("/<int:resource_id>", methods=["PUT"])
def update_resource_route(resource_id):
    try:
        data = ResourceUpdate.model_validate(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid request data",
            "details": error.errors(),
        }), 400

    changes = data.model_dump(exclude_unset=True)

    if not changes:
        return jsonify({
            "error": "Provide at least one field to update"
        }), 400

    db = get_db_session()
    try:
        resource = find_resource(db, resource_id)
        if resource is None:
            return jsonify({"error": "Resource not found"}), 404

        resource = edit_resource(db, resource, **changes)
        return jsonify(resource_to_dict(resource)), 200
    finally:
        db.close()


@resource_bp.route("/<int:resource_id>", methods=["DELETE"])
def delete_resource_route(resource_id):
    db = get_db_session()
    try:
        resource = find_resource(db, resource_id)
        if resource is None:
            return jsonify({"error": "Resource not found"}), 404

        remove_resource(db, resource)
        return jsonify({
            "message": "Resource deleted successfully"
        }), 200
    finally:
        db.close()
