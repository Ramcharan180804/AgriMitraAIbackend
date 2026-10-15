from sqlalchemy.orm import Session

from app.data.models.crop import Crop


def create_crop(
    db: Session,
    crop_name: str,
    scientific_name: str | None = None,
    crop_type: str | None = None,
    suitable_soil: str | None = None,
    min_temperature: float | None = None,
    max_temperature: float | None = None,
    min_rainfall: float | None = None,
    max_rainfall: float | None = None,
    description: str | None = None,
):
    crop = Crop(
        crop_name=crop_name,
        scientific_name=scientific_name,
        crop_type=crop_type,
        suitable_soil=suitable_soil,
        min_temperature=min_temperature,
        max_temperature=max_temperature,
        min_rainfall=min_rainfall,
        max_rainfall=max_rainfall,
        description=description,
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return crop


def get_crop_by_id(db: Session, crop_id: int):
    return db.get(Crop, crop_id)


def get_crop_by_name(db: Session, crop_name: str):
    return (
        db.query(Crop)
        .filter(Crop.crop_name.ilike(crop_name))
        .first()
    )


def get_all_crops(db: Session, active_only: bool = True):
    query = db.query(Crop)

    if active_only:
        query = query.filter(Crop.is_active.is_(True))

    return query.order_by(Crop.crop_name).all()


def update_crop(
    db: Session,
    crop_id: int,
    crop_name: str | None = None,
    scientific_name: str | None = None,
    crop_type: str | None = None,
    suitable_soil: str | None = None,
    min_temperature: float | None = None,
    max_temperature: float | None = None,
    min_rainfall: float | None = None,
    max_rainfall: float | None = None,
    description: str | None = None,
    is_active: bool | None = None,
):
    crop = db.get(Crop, crop_id)

    if crop is None:
        return None

    fields = {
        "crop_name": crop_name,
        "scientific_name": scientific_name,
        "crop_type": crop_type,
        "suitable_soil": suitable_soil,
        "min_temperature": min_temperature,
        "max_temperature": max_temperature,
        "min_rainfall": min_rainfall,
        "max_rainfall": max_rainfall,
        "description": description,
        "is_active": is_active,
    }

    for field, value in fields.items():
        if value is not None:
            setattr(crop, field, value)

    db.commit()
    db.refresh(crop)

    return crop


def delete_crop(db: Session, crop_id: int):
    crop = db.get(Crop, crop_id)

    if crop is None:
        return False

    db.delete(crop)
    db.commit()

    return True
