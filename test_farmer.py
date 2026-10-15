from app.data.database.connection import get_db_session
from app.data.repositories.farmer_repository import create_farmer, get_all_farmers

db = get_db_session()

try:
    farmer = create_farmer(
        db=db,
        name="Test Farmer",
        phone="9000000001",
        village="Kodad",
        district="Suryapet",
    )

    print("Farmer saved successfully!")
    print("Farmer ID:", farmer.id)
    print("Farmer Name:", farmer.name)

    farmers = get_all_farmers(db)
    print("Total farmers:", len(farmers))

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()