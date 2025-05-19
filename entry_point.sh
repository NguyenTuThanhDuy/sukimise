#!/bin/bash

# Wait for database (optional if DB isn't ready instantly)
echo "Waiting for database..."
sleep 3  # or use wait-for-it or similar

echo "$(pip freeze) | grep environ"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
