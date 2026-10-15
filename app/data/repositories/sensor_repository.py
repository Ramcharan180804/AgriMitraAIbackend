from datetime import datetime

from sqlalchemy.orm import Session

from app.data.models.sensor import Sensor


def create_sensor_reading(
    db: Session,
    farm_id: int,
    sensor_type: str,
    value: float,
    unit: str,
    recorded_at: datetime | None = None,
):
    reading = Sensor(
        farm_id=farm_id,
        sensor_type=sensor_type,
        value=value,
        unit=unit,
        recorded_at=recorded_at,
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading


def get_sensor_reading_by_id(db: Session, reading_id: int):
    return db.get(Sensor, reading_id)


def get_sensor_readings_by_farm(
    db: Session,
    farm_id: int,
    limit: int = 100,
):
    return (
        db.query(Sensor)
        .filter(Sensor.farm_id == farm_id)
        .order_by(Sensor.recorded_at.desc(), Sensor.id.desc())
        .limit(limit)
        .all()
    )


def get_latest_sensor_reading(
    db: Session,
    farm_id: int,
    sensor_type: str,
):
    return (
        db.query(Sensor)
        .filter(
            Sensor.farm_id == farm_id,
            Sensor.sensor_type == sensor_type,
        )
        .order_by(Sensor.recorded_at.desc(), Sensor.id.desc())
        .first()
    )


def get_all_sensor_readings(db: Session, limit: int = 100):
    return (
        db.query(Sensor)
        .order_by(Sensor.recorded_at.desc(), Sensor.id.desc())
        .limit(limit)
        .all()
    )


def delete_sensor_reading(db: Session, reading_id: int):
    reading = db.get(Sensor, reading_id)

    if reading is None:
        return False

    db.delete(reading)
    db.commit()

    return True
