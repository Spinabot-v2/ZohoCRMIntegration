import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into os.environ

class Config:
    client_id = os.getenv("ZOHO_CLIENT_ID", "default_client_id")
    client_secret = os.getenv("ZOHO_CLIENT_SECRET", "default_client_secret")
    redirect_uri = os.getenv("ZOHO_REDIRECT_URI", "default_redirect_uri")
    database_name = os.getenv("DEV_DATABASE_NAME", "default_database_name")
    database_user = os.getenv("DEV_DB_USER", "default_db_user")
    database_pass = os.getenv("DEV_DB_PASSWORD", "default_db_password")
    database_host = os.getenv("DEV_CONNECTION_NAME", "default_connection_name")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    redis_host = os.getenv("DEV_CACHE_REDIS_HOST", "default_redis_host")
    redis_port = os.getenv("DEV_CACHE_REDIS_PORT", "default_redis_port")
    redis_username = os.getenv("DEV_CACHE_REDIS_USERNAME", "default_redis_username")
    redis_password = os.getenv("DEV_CACHE_REDIS_PASSWORD", "default_redis_password")