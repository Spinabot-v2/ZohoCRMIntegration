#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is up!"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis is up!" 

echo "Running DB setup..."
python create_db.py

echo "Running migrations..."
mkdir -p migrations/versions

alembic upgrade head

if [ "$ENV" = "dev" ]; then
  echo "Running in development mode"
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
else
  echo "Running in production mode"
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
fi
