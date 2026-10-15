from app.data.repositories.farmer_repository import (
    create_farmer,
    get_farmer_by_id,
    get_all_farmers,
    update_farmer,
    delete_farmer,
)


def create_farmer_service(db, name, phone, village=None, district=None):
    return create_farmer(
        db=db,
        name=name,
        phone=phone,
        village=village,
        district=district,
    )


def get_farmer_service(db, farmer_id):
    return get_farmer_by_id(db, farmer_id)


def get_all_farmers_service(db):
    return get_all_farmers(db)


def update_farmer_service(
    db,
    farmer_id,
    name=None,
    phone=None,
    village=None,
    district=None,
):
    return update_farmer(
        db=db,
        farmer_id=farmer_id,
        name=name,
        phone=phone,
        village=village,
        district=district,
    )


def delete_farmer_service(db, farmer_id):
    return delete_farmer(db, farmer_id)
