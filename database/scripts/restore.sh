#!/bin/bash

# Database Restore Script
# Usage: ./restore.sh <backup_file>

set -e

# Configuration
CONTAINER_NAME="chat-postgres"
DB_NAME="chatdb"
DB_USER="chatuser"
BACKUP_DIR="./scripts/backups"

# Check if backup file is provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Please provide a backup file"
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -la "$BACKUP_DIR"/*.gz 2>/dev/null || echo "No backups found in $BACKUP_DIR"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    # Try looking in backup directory
    if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
        BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE"
    else
        echo "❌ Error: Backup file '$BACKUP_FILE' not found"
        exit 1
    fi
fi

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "❌ Error: PostgreSQL container '$CONTAINER_NAME' is not running"
    echo "Start it with: docker-compose up -d postgres"
    exit 1
fi

echo "🔄 Restoring database from backup..."
echo "📦 Container: $CONTAINER_NAME"
echo "🗃️  Database: $DB_NAME"
echo "📄 Backup file: $BACKUP_FILE"

# Confirm restore
read -p "⚠️  This will overwrite the existing database. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Restore cancelled"
    exit 1
fi

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "📦 Decompressing backup..."
    TEMP_FILE="/tmp/$(basename "$BACKUP_FILE" .gz)"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    BACKUP_FILE="$TEMP_FILE"
fi

# Restore database
echo "🔄 Restoring database..."
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Database restored successfully!"
    
    # Clean up temp file if created
    if [[ -n "$TEMP_FILE" && -f "$TEMP_FILE" ]]; then
        rm "$TEMP_FILE"
    fi
    
    # Show database info
    echo "📊 Database status:"
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) as message_count FROM messages;"
else
    echo "❌ Restore failed!"
    exit 1
fi
