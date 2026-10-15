
from app.data.database.connection import get_db_session
from app.data.repositories.farmer_repository import (
    get_farmer_by_id,
    update_farmer,
)

db = get_db_session()

try:
    farmer = get_farmer_by_id(db, 1)

    if farmer is None:
        print("Farmer ID 1 not found.")

    else:
        print("Before update:", farmer.name)

        updated_farmer = update_farmer(
            db=db,
            farmer_id=1,
            name="Updated Farmer",
            village="Kodad",
            district="Suryapet",
        )

        print("Farmer updated successfully!")
        print("Updated name:", updated_farmer.name)

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()

