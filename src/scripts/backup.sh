#!/bin/bash

set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting backup process..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
echo "Backing up database..."
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_DIR/db_backup_$DATE.sql

# Backup media files
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz -C /app/media .

echo "Backup completed:"
echo "Database: $BACKUP_DIR/db_backup_$DATE.sql"
echo "Media: $BACKUP_DIR/media_backup_$DATE.tar.gz"
