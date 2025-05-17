# create_db.py
from main import app
from database.schemas import create_tables
import time 
# Import db and models inside the context where they're needed
from main import db
from database.schemas import ZohoCreds ,Clients  # Assuming Credentials is the model for the credentials table

with app.app_context():
    # Create tables
    create_tables()
    print("Database tables created!")
    
    # Check if remodel_id=1 is already present in the database
    existing_credential = ZohoCreds.query.filter_by(remodel_id=1).first()
    if not existing_credential:
        # Adding refresh token data so pytests can run without authorization
        TEST_CREDENTIAL = ZohoCreds(
            remodel_id=1,
            access_token="dummy_access_token",
            refresh_token="1000.4f3db5728bf104834e81cc9c117ed326.9964fe2adb4fbe7b0aca8c6a29675210",  # For refresh only refresh token is required
            # Set expiration time to a past timestamp to indicate expired
            expiration_time=int(time.time()) - 1000  # Example: 1000 seconds before current time
        )
        db.session.add(TEST_CREDENTIAL)
        db.session.commit()
        print("TEST data added to credentials table!")
    else:
        print("Data with remodel_id=1 already exists in the credentials table!")
     #update teh clients table to put remodel_id = 1 dev account details in it . 
    existing_CRM_user = Clients.query.filter_by(remodel_id=1).first()
    if not existing_CRM_user:
        # Adding dummy data to Clients table
        TEST_CLIENT = Clients(
            zoho_id="6707647000000503001",
            remodel_id=1,
            full_name="karhteek V"
        )
        db.session.add(TEST_CLIENT)
        db.session.commit()
        print("TEST data added to clients table!")
    else:
        print("Data with remodel_id=1 already exists in the clients table!")