from sqlalchemy.orm import Session

from app.data.repositories.disease_detection_repository import (
    create_disease_detection,
    get_disease_detection_by_id,
    get_disease_detections_by_farm,
    get_all_disease_detections,
    delete_disease_detection,
)


def save_disease_detection(
    db: Session,
    farm_id: int,
    disease_name: str,
    crop_id: int | None = None,
    image_path: str | None = None,
    confidence_score: float | None = None,
    symptoms: str | None = None,
    recommended_treatment: str | None = None,
):
    return create_disease_detection(
        db=db,
        farm_id=farm_id,
        disease_name=disease_name,
        crop_id=crop_id,
        image_path=image_path,
        confidence_score=confidence_score,
        symptoms=symptoms,
        recommended_treatment=recommended_treatment,
    )


def find_disease_detection(
    db: Session, detection_id: int
):
    return get_disease_detection_by_id(db, detection_id)


def find_disease_detections_by_farm(
    db: Session, farm_id: int
):
    return get_disease_detections_by_farm(db, farm_id)


def find_all_disease_detections(
    db: Session, limit: int = 100
):
    return get_all_disease_detections(db, limit)


def remove_disease_detection(
    db: Session, detection
):
    delete_disease_detection(db, detection)
