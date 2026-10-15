from app.data.repositories.crop_repository import (
    create_crop,
    get_crop_by_id,
    get_crop_by_name,
    get_all_crops,
    update_crop,
    delete_crop,
)


def create_crop_service(
    db,
    crop_name,
    scientific_name=None,
    crop_type=None,
    suitable_soil=None,
    min_temperature=None,
    max_temperature=None,
    min_rainfall=None,
    max_rainfall=None,
    description=None,
):
    return create_crop(
        db=db,
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


def get_crop_service(db, crop_id):
    return get_crop_by_id(db, crop_id)


def get_crop_by_name_service(db, crop_name):
    return get_crop_by_name(db, crop_name)


def get_all_crops_service(db, active_only=True):
    return get_all_crops(db, active_only=active_only)


def update_crop_service(
    db,
    crop_id,
    crop_name=None,
    scientific_name=None,
    crop_type=None,
    suitable_soil=None,
    min_temperature=None,
    max_temperature=None,
    min_rainfall=None,
    max_rainfall=None,
    description=None,
    is_active=None,
):
    return update_crop(
        db=db,
        crop_id=crop_id,
        crop_name=crop_name,
        scientific_name=scientific_name,
        crop_type=crop_type,
        suitable_soil=suitable_soil,
        min_temperature=min_temperature,
        max_temperature=max_temperature,
        min_rainfall=min_rainfall,
        max_rainfall=max_rainfall,
        description=description,
        is_active=is_active,
    )


def delete_crop_service(db, crop_id):
    return delete_crop(db, crop_id)
