from app.data.repositories.sensor_repository import (
    create_sensor_reading,
    get_sensor_reading_by_id,
    get_sensor_readings_by_farm,
    get_latest_sensor_reading,
    get_all_sensor_readings,
    delete_sensor_reading,
)


def create_sensor_reading_service(
    db,
    farm_id,
    sensor_type,
    value,
    unit,
    recorded_at=None,
):
    return create_sensor_reading(
        db=db,
        farm_id=farm_id,
        sensor_type=sensor_type,
        value=value,
        unit=unit,
        recorded_at=recorded_at,
    )


def get_sensor_reading_service(db, reading_id):
    return get_sensor_reading_by_id(db, reading_id)


def get_sensor_readings_by_farm_service(db, farm_id, limit=100):
    return get_sensor_readings_by_farm(
        db=db,
        farm_id=farm_id,
        limit=limit,
    )


def get_latest_sensor_reading_service(db, farm_id, sensor_type):
    return get_latest_sensor_reading(
        db=db,
        farm_id=farm_id,
        sensor_type=sensor_type,
    )


def get_all_sensor_readings_service(db, limit=100):
    return get_all_sensor_readings(db=db, limit=limit)


def delete_sensor_reading_service(db, reading_id):
    return delete_sensor_reading(db, reading_id)
