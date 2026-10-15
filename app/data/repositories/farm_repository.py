from sqlalchemy.orm import Session

from app.data.models.farm import Farm


def create_farm(
    db: Session,
    farm_name: str,
    area_acres: float,
    farmer_id: int,
    location: str | None = None,
    district: str | None = None,
    village: str | None = None,
):
    farm = Farm(
        farm_name=farm_name,
        area_acres=area_acres,
        farmer_id=farmer_id,
        location=location,
        district=district,
        village=village,
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


def get_farm_by_id(db: Session, farm_id: int):
    return db.get(Farm, farm_id)


def get_farms_by_farmer(db: Session, farmer_id: int):
    return (
        db.query(Farm)
        .filter(Farm.farmer_id == farmer_id)
        .order_by(Farm.id)
        .all()
    )


def get_all_farms(db: Session):
    return db.query(Farm).order_by(Farm.id).all()


def update_farm(
    db: Session,
    farm_id: int,
    farm_name: str | None = None,
    area_acres: float | None = None,
    location: str | None = None,
    district: str | None = None,
    village: str | None = None,
):
    farm = db.get(Farm, farm_id)

    if farm is None:
        return None

    if farm_name is not None:
        farm.farm_name = farm_name

    if area_acres is not None:
        farm.area_acres = area_acres

    if location is not None:
        farm.location = location

    if district is not None:
        farm.district = district

    if village is not None:
        farm.village = village

    db.commit()
    db.refresh(farm)

    return farm


def delete_farm(db: Session, farm_id: int):
    farm = db.get(Farm, farm_id)

    if farm is None:
        return False

    db.delete(farm)
    db.commit()

    return True
