from app.data.models.evaluation import Evaluation


def create_evaluation(
    db,
    farm_id,
    crop_name,
    yield_quantity,
    quality_rating,
    total_cost=0,
    profit=None,
    notes=None,
):
    evaluation = Evaluation(
        farm_id=farm_id,
        crop_name=crop_name,
        yield_quantity=yield_quantity,
        quality_rating=quality_rating,
        total_cost=total_cost,
        profit=profit,
        notes=notes,
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def get_evaluation_by_id(db, evaluation_id):
    return (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )


def get_evaluations_by_farm(db, farm_id):
    return (
        db.query(Evaluation)
        .filter(Evaluation.farm_id == farm_id)
        .order_by(Evaluation.evaluated_at.desc())
        .all()
    )


def get_all_evaluations(db, limit=100):
    return (
        db.query(Evaluation)
        .order_by(Evaluation.evaluated_at.desc())
        .limit(limit)
        .all()
    )


def update_evaluation(db, evaluation, data):
    for field, value in data.items():
        if hasattr(evaluation, field):
            setattr(evaluation, field, value)

    db.commit()
    db.refresh(evaluation)
    return evaluation


def delete_evaluation(db, evaluation):
    db.delete(evaluation)
    db.commit()
