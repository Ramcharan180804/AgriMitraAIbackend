from app.data.repositories.farm_repository import (
    create_farm,
    get_farm_by_id,
    get_farms_by_farmer,
    get_all_farms,
    update_farm,
    delete_farm,
)


def create_farm_service(
    db,
    farm_name,
    area_acres,
    farmer_id,
    location=None,
    district=None,
    village=None,
):
    return create_farm(
        db=db,
        farm_name=farm_name,
        area_acres=area_acres,
        farmer_id=farmer_id,
        location=location,
        district=district,
        village=village,
    )


def get_farm_service(db, farm_id):
    return get_farm_by_id(db, farm_id)


def get_farms_by_farmer_service(db, farmer_id):
    return get_farms_by_farmer(db, farmer_id)


def get_all_farms_service(db):
    return get_all_farms(db)


def update_farm_service(
    db,
    farm_id,
    farm_name=None,
    area_acres=None,
    location=None,
    district=None,
    village=None,
):
    return update_farm(
        db=db,
        farm_id=farm_id,
        farm_name=farm_name,
        area_acres=area_acres,
        location=location,
        district=district,
        village=village,
    )


def delete_farm_service(db, farm_id):
    return delete_farm(db, farm_id)
