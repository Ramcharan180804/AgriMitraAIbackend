from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.resource import Resource


def create_resource(
    db: Session,
    resource_name: str,
    resource_type: str,
    unit: str,
    price_per_unit: float,
    available_quantity: float = 0,
    description: str | None = None,
    is_available: bool = True,
) -> Resource:
    resource = Resource(
        resource_name=resource_name,
        resource_type=resource_type,
        unit=unit,
        price_per_unit=price_per_unit,
        available_quantity=available_quantity,
        description=description,
        is_available=is_available,
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def get_resource_by_id(
    db: Session, resource_id: int
) -> Resource | None:
    return db.get(Resource, resource_id)


def get_all_resources(
    db: Session,
    available_only: bool = False,
    limit: int = 100,
) -> list[Resource]:
    statement = select(Resource).order_by(Resource.id.desc())

    if available_only:
        statement = statement.where(Resource.is_available.is_(True))

    statement = statement.limit(limit)
    return list(db.scalars(statement).all())


def search_resources_by_type(
    db: Session, resource_type: str
) -> list[Resource]:
    statement = (
        select(Resource)
        .where(Resource.resource_type.ilike(resource_type))
        .order_by(Resource.resource_name)
    )
    return list(db.scalars(statement).all())


def update_resource(
    db: Session,
    resource: Resource,
    **changes,
) -> Resource:
    allowed_fields = {
        "resource_name",
        "resource_type",
        "description",
        "unit",
        "price_per_unit",
        "available_quantity",
        "is_available",
    }

    for field, value in changes.items():
        if field in allowed_fields:
            setattr(resource, field, value)

    db.commit()
    db.refresh(resource)
    return resource


def delete_resource(
    db: Session, resource: Resource
) -> None:
    db.delete(resource)
    db.commit()
