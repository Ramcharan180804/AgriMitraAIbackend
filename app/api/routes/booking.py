from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.data.database.connection import get_db_session
from app.data.schemas.booking import (
    BookingCreate,
    BookingStatusUpdate,
    BookingResponse,
)
from app.services.booking_service import (
    BookingError,
    create_farmer_booking,
    find_booking,
    find_bookings_by_farmer,
    find_all_bookings,
    change_booking_status,
    remove_booking,
)

booking_bp = Blueprint(
    "bookings", __name__, url_prefix="/api/bookings"
)


def booking_to_dict(booking):
    return BookingResponse.model_validate(booking).model_dump(mode="json")


@booking_bp.route("", methods=["POST"])
def create_booking_route():
    try:
        data = BookingCreate.model_validate(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid request data",
            "details": error.errors(),
        }), 400

    db = get_db_session()
    try:
        booking = create_farmer_booking(
            db=db,
            farmer_id=data.farmer_id,
            resource_id=data.resource_id,
            quantity=data.quantity,
            notes=data.notes,
        )
        return jsonify(booking_to_dict(booking)), 201
    except BookingError as error:
        return jsonify({"error": str(error)}), 400
    except IntegrityError:
        db.rollback()
        return jsonify({
            "error": "Farmer or resource ID does not exist"
        }), 400
    finally:
        db.close()


@booking_bp.route("", methods=["GET"])
def get_all_bookings_route():
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
        bookings = find_all_bookings(db, limit)
        return jsonify([booking_to_dict(item) for item in bookings]), 200
    finally:
        db.close()


@booking_bp.route("/farmer/<int:farmer_id>", methods=["GET"])
def get_bookings_by_farmer_route(farmer_id):
    db = get_db_session()
    try:
        bookings = find_bookings_by_farmer(db, farmer_id)
        return jsonify([booking_to_dict(item) for item in bookings]), 200
    finally:
        db.close()


@booking_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking_route(booking_id):
    db = get_db_session()
    try:
        booking = find_booking(db, booking_id)
        if booking is None:
            return jsonify({"error": "Booking not found"}), 404

        return jsonify(booking_to_dict(booking)), 200
    finally:
        db.close()


@booking_bp.route("/<int:booking_id>/status", methods=["PATCH"])
def update_booking_status_route(booking_id):
    try:
        data = BookingStatusUpdate.model_validate(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid request data",
            "details": error.errors(),
        }), 400

    db = get_db_session()
    try:
        booking = change_booking_status(
            db=db,
            booking_id=booking_id,
            new_status=data.booking_status,
        )
        return jsonify(booking_to_dict(booking)), 200
    except BookingError as error:
        return jsonify({"error": str(error)}), 400
    finally:
        db.close()


@booking_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking_route(booking_id):
    db = get_db_session()
    try:
        remove_booking(db, booking_id)
        return jsonify({
            "message": "Booking deleted successfully"
        }), 200
    except BookingError as error:
        status_code = 404 if str(error) == "Booking not found." else 400
        return jsonify({"error": str(error)}), status_code
    finally:
        db.close()
