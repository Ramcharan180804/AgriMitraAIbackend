from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.data.database.connection import get_db_session
from app.data.schemas.evaluation import (
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationResponse,
)
from app.services.evaluation_service import (
    add_evaluation,
    find_evaluation,
    find_evaluations_by_farm,
    find_all_evaluations,
    edit_evaluation,
    remove_evaluation,
)

evaluation_bp = Blueprint(
    "evaluation",
    __name__,
    url_prefix="/api/evaluations",
)


def evaluation_to_dict(evaluation):
    return EvaluationResponse.model_validate(evaluation).model_dump(mode="json")


@evaluation_bp.route("", methods=["POST"])
def create_evaluation_route():
    db = get_db_session()
    try:
        data = EvaluationCreate.model_validate(
            request.get_json(silent=True) or {}
        )

        evaluation = add_evaluation(
            db=db,
            farm_id=data.farm_id,
            crop_name=data.crop_name,
            yield_quantity=data.yield_quantity,
            quality_rating=data.quality_rating,
            total_cost=data.total_cost,
            profit=data.profit,
            notes=data.notes,
        )
        return jsonify(evaluation_to_dict(evaluation)), 201

    except ValidationError as error:
        db.rollback()
        return jsonify({
            "error": "Validation failed",
            "details": error.errors(include_url=False),
        }), 400
    except ValueError as error:
        db.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.rollback()
        return jsonify({"error": "Could not create evaluation"}), 500
    finally:
        db.close()


@evaluation_bp.route("", methods=["GET"])
def get_all_evaluations_route():
    db = get_db_session()
    try:
        limit = request.args.get("limit", default=100, type=int)
        evaluations = find_all_evaluations(db, limit)
        return jsonify([
            evaluation_to_dict(item) for item in evaluations
        ]), 200
    finally:
        db.close()


@evaluation_bp.route("/farm/<int:farm_id>", methods=["GET"])
def get_evaluations_by_farm_route(farm_id):
    db = get_db_session()
    try:
        evaluations = find_evaluations_by_farm(db, farm_id)
        return jsonify([
            evaluation_to_dict(item) for item in evaluations
        ]), 200
    finally:
        db.close()


@evaluation_bp.route("/<int:evaluation_id>", methods=["GET"])
def get_evaluation_route(evaluation_id):
    db = get_db_session()
    try:
        evaluation = find_evaluation(db, evaluation_id)
        if evaluation is None:
            return jsonify({"error": "Evaluation not found"}), 404
        return jsonify(evaluation_to_dict(evaluation)), 200
    finally:
        db.close()


@evaluation_bp.route("/<int:evaluation_id>", methods=["PUT"])
def update_evaluation_route(evaluation_id):
    db = get_db_session()
    try:
        data = EvaluationUpdate.model_validate(
            request.get_json(silent=True) or {}
        )
        updates = data.model_dump(exclude_unset=True)

        if not updates:
            return jsonify({
                "error": "Provide at least one field to update"
            }), 400

        evaluation = edit_evaluation(db, evaluation_id, updates)
        if evaluation is None:
            return jsonify({"error": "Evaluation not found"}), 404

        return jsonify(evaluation_to_dict(evaluation)), 200

    except ValidationError as error:
        db.rollback()
        return jsonify({
            "error": "Validation failed",
            "details": error.errors(include_url=False),
        }), 400
    except ValueError as error:
        db.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.rollback()
        return jsonify({"error": "Could not update evaluation"}), 500
    finally:
        db.close()


@evaluation_bp.route("/<int:evaluation_id>", methods=["DELETE"])
def delete_evaluation_route(evaluation_id):
    db = get_db_session()
    try:
        deleted = remove_evaluation(db, evaluation_id)
        if not deleted:
            return jsonify({"error": "Evaluation not found"}), 404

        return jsonify({
            "message": "Evaluation deleted successfully"
        }), 200
    finally:
        db.close()
