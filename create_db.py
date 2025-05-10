# create_db.py
from main import app
from database.schemas import create_tables

# Import db inside the context where it's needed
from main import db

with app.app_context():
    create_tables()
    print("Database tables created!")
