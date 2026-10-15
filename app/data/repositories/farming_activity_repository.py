from app.data.models.farming_activity import FarmingActivity


def create_farming_activity(
    db,
    farm_id,
    activity_type,
    description=None,
    resource_used=None,
    quantity_used=None,
    cost=0,
    notes=None,
):
    activity = FarmingActivity(
        farm_id=farm_id,
        activity_type=activity_type,
        description=description,
        resource_used=resource_used,
        quantity_used=quantity_used,
        cost=cost,
        notes=notes,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_farming_activity_by_id(db, activity_id):
    return (
        db.query(FarmingActivity)
        .filter(FarmingActivity.id == activity_id)
        .first()
    )


def get_farming_activities_by_farm(db, farm_id):
    return (
        db.query(FarmingActivity)
        .filter(FarmingActivity.farm_id == farm_id)
        .order_by(FarmingActivity.activity_date.desc())
        .all()
    )


def get_all_farming_activities(db, limit=100):
    return (
        db.query(FarmingActivity)
        .order_by(FarmingActivity.activity_date.desc())
        .limit(limit)
        .all()
    )


def update_farming_activity(db, activity, data):
    for field, value in data.items():
        if hasattr(activity, field):
            setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity


def delete_farming_activity(db, activity):
    db.delete(activity)
    db.commit()
