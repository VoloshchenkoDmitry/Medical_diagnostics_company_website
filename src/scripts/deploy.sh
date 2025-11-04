#!/bin/bash

set -e

echo "Starting deployment process..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
fi

# Build and start services
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser if not exists (опционально)
# docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --noinput || true

echo "Deployment completed successfully!"
echo "Application is running on http://localhost"
