#!/bin/bash

# Database Backup Script
# Usage: ./backup.sh [backup_name]

set -e

# Configuration
CONTAINER_NAME="chat-postgres"
DB_NAME="chatdb"
DB_USER="chatuser"
BACKUP_DIR="./scripts/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME=${1:-"backup_${TIMESTAMP}"}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Error: PostgreSQL container '$CONTAINER_NAME' is not running"
    echo "Start it with: docker-compose up -d postgres"
    exit 1
fi

echo "🗄️  Creating database backup..."
echo "📅 Timestamp: $TIMESTAMP"
echo "📦 Container: $CONTAINER_NAME"
echo "🗃️  Database: $DB_NAME"

# Create backup
docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --clean --if-exists > "$BACKUP_DIR/${BACKUP_NAME}.sql"

if [ $? -eq 0 ]; then
    echo "✅ Backup created successfully: $BACKUP_DIR/${BACKUP_NAME}.sql"
    
    # Compress backup
    gzip "$BACKUP_DIR/${BACKUP_NAME}.sql"
    echo "📦 Backup compressed: $BACKUP_DIR/${BACKUP_NAME}.sql.gz"
    
    # Show backup info
    echo "📊 Backup size: $(du -h "$BACKUP_DIR/${BACKUP_NAME}.sql.gz" | cut -f1)"
    
    # List recent backups
    echo "📋 Recent backups:"
    ls -lah "$BACKUP_DIR"/*.gz | tail -5
else
    echo "❌ Backup failed!"
    exit 1
fi
