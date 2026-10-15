
from app.data.database.connection import get_db_session
from app.data.repositories.farmer_repository import (
    create_farmer,
    delete_farmer,
    get_farmer_by_id,
)

db = get_db_session()

try:
    # Create a separate test farmer
    farmer = create_farmer(
        db=db,
        name="Delete Test Farmer",
        phone="9000000099",
        village="Test Village",
        district="Test District",
    )

    farmer_id = farmer.id
    print("Test farmer created. ID:", farmer_id)

    # Delete only the test farmer
    deleted = delete_farmer(db, farmer_id)

    if deleted:
        print("Test farmer deleted successfully!")

    # Verify that the record no longer exists
    remaining_farmer = get_farmer_by_id(db, farmer_id)

    if remaining_farmer is None:
        print("Delete verification successful!")
    else:
        print("Test farmer still exists.")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()

