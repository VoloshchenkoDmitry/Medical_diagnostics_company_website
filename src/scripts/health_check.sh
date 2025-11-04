#!/bin/bash

set -e

echo "Performing health check..."

# Check if web service is responding
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    echo "✓ Web service is healthy"
else
    echo "✗ Web service is not responding"
    exit 1
fi

# Check database connection
if docker-compose -f docker-compose.prod.yml exec db pg_isready -U $POSTGRES_USER -d $POSTGRES_DB > /dev/null 2>&1; then
    echo "✓ Database is healthy"
else
    echo "✗ Database is not responding"
    exit 1
fi

echo "All services are healthy!"
