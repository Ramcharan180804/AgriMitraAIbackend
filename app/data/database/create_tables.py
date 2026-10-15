from app.data.database.connection import engine
from app.data.database.models import Base

# Import models so SQLAlchemy registers their tables.
from app.data.models.farmer import Farmer
from app.data.models.farm import Farm


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
