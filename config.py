import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into os.environ

class Config:
    client_id = os.getenv("ZOHO_CLIENT_ID")
    client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    database_name = os.getenv("DEV_DATABASE_NAME")
    database_user = os.getenv("DEV_DB_USER")
    database_pass = os.getenv("DEV_DB_PASSWORD")
    database_host = os.getenv("DEV_CONNECTION_NAME")
    SECRET_KEY = 'SECRET-KEY-FLASK-APP'