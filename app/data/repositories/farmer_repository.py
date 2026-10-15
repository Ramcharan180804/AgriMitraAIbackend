from sqlalchemy.orm import Session

from app.data.models.farmer import Farmer


def create_farmer(
    db: Session,
    name: str,
    phone: str,
    village: str | None = None,
    district: str | None = None,
):
    farmer = Farmer(
        name=name,
        phone=phone,
        village=village,
        district=district,
    )

    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    return farmer


def get_farmer_by_id(db: Session, farmer_id: int):
    return db.get(Farmer, farmer_id)


def get_all_farmers(db: Session):
    return db.query(Farmer).order_by(Farmer.id).all()
# UPDATE: Modify existing farmer details
def update_farmer(
    db: Session,
    farmer_id: int,
    name: str | None = None,
    phone: str | None = None,
    village: str | None = None,
    district: str | None = None,
):
    farmer = db.get(Farmer, farmer_id)

    if farmer is None:
        return None

    if name is not None:
        farmer.name = name
    if phone is not None:
        farmer.phone = phone
    if village is not None:
        farmer.village = village
    if district is not None:
        farmer.district = district

    db.commit()
    db.refresh(farmer)
    return farmer


# DELETE: Remove farmer by ID
def delete_farmer(db: Session, farmer_id: int):
    farmer = db.get(Farmer, farmer_id)

    if farmer is None:
        return False

    db.delete(farmer)
    db.commit()
    return True
