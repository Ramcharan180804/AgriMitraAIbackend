from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.disease_detection import DiseaseDetection


def create_disease_detection(
    db: Session,
    farm_id: int,
    disease_name: str,
    crop_id: int | None = None,
    image_path: str | None = None,
    confidence_score: float | None = None,
    symptoms: str | None = None,
    recommended_treatment: str | None = None,
) -> DiseaseDetection:
    detection = DiseaseDetection(
        farm_id=farm_id,
        crop_id=crop_id,
        disease_name=disease_name,
        image_path=image_path,
        confidence_score=confidence_score,
        symptoms=symptoms,
        recommended_treatment=recommended_treatment,
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


def get_disease_detection_by_id(
    db: Session, detection_id: int
) -> DiseaseDetection | None:
    return db.get(DiseaseDetection, detection_id)


def get_disease_detections_by_farm(
    db: Session, farm_id: int
) -> list[DiseaseDetection]:
    statement = (
        select(DiseaseDetection)
        .where(DiseaseDetection.farm_id == farm_id)
        .order_by(DiseaseDetection.detected_at.desc())
    )
    return list(db.scalars(statement).all())


def get_all_disease_detections(
    db: Session, limit: int = 100
) -> list[DiseaseDetection]:
    statement = (
        select(DiseaseDetection)
        .order_by(DiseaseDetection.detected_at.desc())
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def delete_disease_detection(
    db: Session, detection: DiseaseDetection
) -> None:
    db.delete(detection)
    db.commit()
