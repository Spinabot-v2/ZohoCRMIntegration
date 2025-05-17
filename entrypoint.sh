#!/bin/bash
echo "Running DB setup..."
python create_db.py

echo "Running migrations..."
mkdir -p migrations/versions

alembic upgrade head

echo "Initializing database..."
# Set the FLASK_APP environment variable
export FLASK_APP=main.py
# Run the Flask CLI command to initialize the database
flask db init


echo "Starting application..."
# Start the application with Gunicorn using env vars
gunicorn -w "$GUNICORN_WORKERS" -k "$GUNICORN_CLASS" -b "$GUNICORN_HOST" main:app