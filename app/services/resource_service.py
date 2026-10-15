from sqlalchemy.orm import Session

from app.data.repositories.resource_repository import (
    create_resource,
    get_resource_by_id,
    get_all_resources,
    search_resources_by_type,
    update_resource,
    delete_resource,
)


def save_resource(
    db: Session,
    resource_name: str,
    resource_type: str,
    unit: str,
    price_per_unit: float,
    available_quantity: float = 0,
    description: str | None = None,
    is_available: bool = True,
):
    return create_resource(
        db=db,
        resource_name=resource_name,
        resource_type=resource_type,
        unit=unit,
        price_per_unit=price_per_unit,
        available_quantity=available_quantity,
        description=description,
        is_available=is_available,
    )


def find_resource(db: Session, resource_id: int):
    return get_resource_by_id(db, resource_id)


def find_all_resources(
    db: Session,
    available_only: bool = False,
    limit: int = 100,
):
    return get_all_resources(
        db,
        available_only=available_only,
        limit=limit,
    )


def find_resources_by_type(
    db: Session, resource_type: str
):
    return search_resources_by_type(db, resource_type)


def edit_resource(db: Session, resource, **changes):
    return update_resource(db, resource, **changes)


def remove_resource(db: Session, resource):
    delete_resource(db, resource)
