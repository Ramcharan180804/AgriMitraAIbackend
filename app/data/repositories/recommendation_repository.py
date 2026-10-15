from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.recommendation import Recommendation


def create_recommendation(
    db: Session,
    farm_id: int,
    crop_id: int,
    confidence_score: float | None = None,
    recommendation_reason: str | None = None,
    season: str | None = None,
) -> Recommendation:
    recommendation = Recommendation(
        farm_id=farm_id,
        crop_id=crop_id,
        confidence_score=confidence_score,
        recommendation_reason=recommendation_reason,
        season=season,
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def get_recommendation_by_id(
    db: Session, recommendation_id: int
) -> Recommendation | None:
    return db.get(Recommendation, recommendation_id)


def get_recommendations_by_farm(
    db: Session, farm_id: int
) -> list[Recommendation]:
    statement = (
        select(Recommendation)
        .where(Recommendation.farm_id == farm_id)
        .order_by(Recommendation.created_at.desc())
    )
    return list(db.scalars(statement).all())


def get_all_recommendations(
    db: Session, limit: int = 100
) -> list[Recommendation]:
    statement = (
        select(Recommendation)
        .order_by(Recommendation.created_at.desc())
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def delete_recommendation(
    db: Session, recommendation: Recommendation
) -> None:
    db.delete(recommendation)
    db.commit()
