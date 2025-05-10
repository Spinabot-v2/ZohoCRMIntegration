#!/bin/bash
# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is up!"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis is up!" 

# Run DB setup Create databae and (creates tables if not there)
echo "Running DB setup..."
python create_db.py

# Run Alembic migrations
echo "Running migrations..."
alembic upgrade head

# Check the environment and start the FastAPI app accordingly
if [ "$ENV" = "dev" ]; then
  echo "Running in development mode"
  gunicorn -w 4 -b 0.0.0.0:5000 main:app

else
  echo "Running in production mode"
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
fi
