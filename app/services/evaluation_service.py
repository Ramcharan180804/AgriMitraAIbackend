from app.data.repositories.evaluation_repository import (
    create_evaluation,
    get_evaluation_by_id,
    get_evaluations_by_farm,
    get_all_evaluations,
    update_evaluation,
    delete_evaluation,
)


def add_evaluation(
    db,
    farm_id,
    crop_name,
    yield_quantity,
    quality_rating,
    total_cost=0,
    profit=None,
    notes=None,
):
    if farm_id <= 0:
        raise ValueError("Farm ID must be positive.")

    if not crop_name or not crop_name.strip():
        raise ValueError("Crop name is required.")

    if yield_quantity < 0:
        raise ValueError("Yield quantity cannot be negative.")

    if not 0 <= quality_rating <= 10:
        raise ValueError("Quality rating must be between 0 and 10.")

    if total_cost < 0:
        raise ValueError("Total cost cannot be negative.")

    return create_evaluation(
        db=db,
        farm_id=farm_id,
        crop_name=crop_name.strip(),
        yield_quantity=yield_quantity,
        quality_rating=quality_rating,
        total_cost=total_cost,
        profit=profit,
        notes=notes,
    )


def find_evaluation(db, evaluation_id):
    return get_evaluation_by_id(db, evaluation_id)


def find_evaluations_by_farm(db, farm_id):
    return get_evaluations_by_farm(db, farm_id)


def find_all_evaluations(db, limit=100):
    limit = max(1, min(limit, 500))
    return get_all_evaluations(db, limit)


def edit_evaluation(db, evaluation_id, data):
    evaluation = get_evaluation_by_id(db, evaluation_id)

    if evaluation is None:
        return None

    if "crop_name" in data:
        crop_name = data["crop_name"]
        if not isinstance(crop_name, str) or not crop_name.strip():
            raise ValueError("Crop name cannot be empty.")
        data["crop_name"] = crop_name.strip()

    if "yield_quantity" in data and data["yield_quantity"] < 0:
        raise ValueError("Yield quantity cannot be negative.")

    if "quality_rating" in data:
        rating = data["quality_rating"]
        if not 0 <= rating <= 10:
            raise ValueError("Quality rating must be between 0 and 10.")

    if "total_cost" in data and data["total_cost"] < 0:
        raise ValueError("Total cost cannot be negative.")

    return update_evaluation(db, evaluation, data)


def remove_evaluation(db, evaluation_id):
    evaluation = get_evaluation_by_id(db, evaluation_id)

    if evaluation is None:
        return False

    delete_evaluation(db, evaluation)
    return True
