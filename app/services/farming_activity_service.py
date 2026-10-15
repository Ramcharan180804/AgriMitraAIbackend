from app.data.repositories.farming_activity_repository import (
    create_farming_activity,
    get_farming_activity_by_id,
    get_farming_activities_by_farm,
    get_all_farming_activities,
    update_farming_activity,
    delete_farming_activity,
)


def add_farming_activity(
    db,
    farm_id,
    activity_type,
    description=None,
    resource_used=None,
    quantity_used=None,
    cost=0,
    notes=None,
):
    if not activity_type or not activity_type.strip():
        raise ValueError("Activity type is required.")

    if cost < 0:
        raise ValueError("Cost cannot be negative.")

    if quantity_used is not None and quantity_used < 0:
        raise ValueError("Quantity used cannot be negative.")

    return create_farming_activity(
        db=db,
        farm_id=farm_id,
        activity_type=activity_type.strip(),
        description=description,
        resource_used=resource_used,
        quantity_used=quantity_used,
        cost=cost,
        notes=notes,
    )


def find_farming_activity(db, activity_id):
    return get_farming_activity_by_id(db, activity_id)


def find_farming_activities_by_farm(db, farm_id):
    return get_farming_activities_by_farm(db, farm_id)


def find_all_farming_activities(db, limit=100):
    limit = max(1, min(limit, 500))
    return get_all_farming_activities(db, limit)


def edit_farming_activity(db, activity_id, data):
    activity = get_farming_activity_by_id(db, activity_id)

    if activity is None:
        return None

    if "activity_type" in data:
        activity_type = data["activity_type"]

        if not isinstance(activity_type, str) or not activity_type.strip():
            raise ValueError("Activity type cannot be empty.")

        data["activity_type"] = activity_type.strip()

    if "cost" in data and data["cost"] < 0:
        raise ValueError("Cost cannot be negative.")

    if "quantity_used" in data:
        quantity = data["quantity_used"]

        if quantity is not None and quantity < 0:
            raise ValueError("Quantity used cannot be negative.")

    return update_farming_activity(db, activity, data)


def remove_farming_activity(db, activity_id):
    activity = get_farming_activity_by_id(db, activity_id)

    if activity is None:
        return False

    delete_farming_activity(db, activity)
    return True
