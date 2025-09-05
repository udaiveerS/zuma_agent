#!/bin/bash

# Database Management Script
# Provides easy commands for managing the PostgreSQL container

set -e

COMPOSE_FILE="docker-compose.yml"
CONTAINER_NAME="chat-postgres"

show_help() {
    echo "🗄️  Chat Database Management"
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start         Start the database container"
    echo "  stop          Stop the database container"
    echo "  restart       Restart the database container"
    echo "  status        Show container status"
    echo "  logs          Show container logs"
    echo "  shell         Open PostgreSQL shell"
    echo "  backup        Create database backup"
    echo "  restore       Restore database from backup"
    echo "  reset         Reset database (WARNING: deletes all data)"
    echo "  tools         Start with pgAdmin (database management UI)"
    echo ""
    echo "Examples:"
    echo "  $0 start              # Start database"
    echo "  $0 backup my_backup   # Create named backup"
    echo "  $0 restore backup.sql # Restore from backup"
    echo "  $0 tools              # Start with pgAdmin on :8080"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose is not installed"
        exit 1
    fi
}

start_db() {
    echo "🚀 Starting PostgreSQL container..."
    docker-compose up -d postgres
    echo "✅ Database started!"
    echo "📍 Connection: localhost:5432"
    echo "🗃️  Database: chatdb"
    echo "👤 User: chatuser"
}

stop_db() {
    echo "🛑 Stopping PostgreSQL container..."
    docker-compose stop postgres
    echo "✅ Database stopped!"
}

restart_db() {
    echo "🔄 Restarting PostgreSQL container..."
    docker-compose restart postgres
    echo "✅ Database restarted!"
}

show_status() {
    echo "📊 Container Status:"
    docker-compose ps
    echo ""
    if docker ps | grep -q "$CONTAINER_NAME"; then
        echo "🔍 Database Info:"
        docker exec "$CONTAINER_NAME" psql -U chatuser -d chatdb -c "SELECT COUNT(*) as total_messages FROM messages;"
    fi
}

show_logs() {
    echo "📋 Container Logs:"
    docker-compose logs -f postgres
}

open_shell() {
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo "❌ Database container is not running. Start it first with: $0 start"
        exit 1
    fi
    
    echo "🐚 Opening PostgreSQL shell..."
    echo "💡 Tip: Use \\q to exit, \\dt to list tables"
    docker exec -it "$CONTAINER_NAME" psql -U chatuser -d chatdb
}

create_backup() {
    ./scripts/backup.sh "$1"
}

restore_backup() {
    if [ -z "$1" ]; then
        echo "❌ Please specify backup file"
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    ./scripts/restore.sh "$1"
}

reset_db() {
    echo "⚠️  WARNING: This will delete ALL data in the database!"
    read -p "Type 'RESET' to confirm: " -r
    if [[ $REPLY == "RESET" ]]; then
        echo "🗑️  Resetting database..."
        docker-compose down -v postgres
        docker-compose up -d postgres
        echo "✅ Database reset complete!"
    else
        echo "❌ Reset cancelled"
    fi
}

start_tools() {
    echo "🛠️  Starting database with management tools..."
    docker-compose --profile tools up -d
    echo "✅ Services started!"
    echo "📍 Database: localhost:5432"
    echo "🌐 pgAdmin: http://localhost:8080"
    echo "   Email: admin@chat.local"
    echo "   Password: admin123"
}

# Main script logic
case "${1:-}" in
    start)
        check_docker
        start_db
        ;;
    stop)
        check_docker
        stop_db
        ;;
    restart)
        check_docker
        restart_db
        ;;
    status)
        check_docker
        show_status
        ;;
    logs)
        check_docker
        show_logs
        ;;
    shell)
        check_docker
        open_shell
        ;;
    backup)
        check_docker
        create_backup "$2"
        ;;
    restore)
        check_docker
        restore_backup "$2"
        ;;
    reset)
        check_docker
        reset_db
        ;;
    tools)
        check_docker
        start_tools
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: ${1:-}"
        echo ""
        show_help
        exit 1
        ;;
esac
