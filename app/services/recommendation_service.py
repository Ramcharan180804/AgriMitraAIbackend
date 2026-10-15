from sqlalchemy.orm import Session

from app.data.repositories.recommendation_repository import (
    create_recommendation,
    get_recommendation_by_id,
    get_recommendations_by_farm,
    get_all_recommendations,
    delete_recommendation,
)


def save_recommendation(
    db: Session,
    farm_id: int,
    crop_id: int,
    confidence_score: float | None = None,
    recommendation_reason: str | None = None,
    season: str | None = None,
):
    return create_recommendation(
        db=db,
        farm_id=farm_id,
        crop_id=crop_id,
        confidence_score=confidence_score,
        recommendation_reason=recommendation_reason,
        season=season,
    )


def find_recommendation(
    db: Session, recommendation_id: int
):
    return get_recommendation_by_id(db, recommendation_id)


def find_recommendations_by_farm(
    db: Session, farm_id: int
):
    return get_recommendations_by_farm(db, farm_id)


def find_all_recommendations(
    db: Session, limit: int = 100
):
    return get_all_recommendations(db, limit)


def remove_recommendation(db: Session, recommendation):
    delete_recommendation(db, recommendation)
