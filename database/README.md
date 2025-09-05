# Chat Database Container

Containerized PostgreSQL database for the Chat API application, completely decoupled from the backend.

## 🏗️ Architecture

- **Database**: PostgreSQL 16 (Alpine Linux)
- **Container**: Docker with health checks
- **Management**: Docker Compose + custom scripts
- **Persistence**: Docker volumes for data
- **Backup**: Automated backup/restore scripts

## 🚀 Quick Start

### 1. Start Database
```bash
# Simple start
./manage.sh start

# Or with Docker Compose directly
docker-compose up -d postgres
```

### 2. Check Status
```bash
./manage.sh status
```

### 3. Connect from Backend
The backend will automatically connect using these credentials:
- **Host**: `localhost:5432`
- **Database**: `chatdb`
- **User**: `chatuser`
- **Password**: `chatpass`

## 📁 Directory Structure

```
database/
├── docker/
│   └── Dockerfile              # PostgreSQL container definition
├── scripts/
│   ├── init/
│   │   ├── 01-create-tables.sql    # Database schema
│   │   └── 02-create-functions.sql # Utility functions
│   ├── backup.sh               # Backup script
│   ├── restore.sh              # Restore script
│   └── backups/                # Backup storage
├── data/                       # Persistent data (auto-created)
├── docker-compose.yml          # Container orchestration
├── manage.sh                   # Management script
└── README.md                   # This file
```

## 🔧 Management Commands

### Essential Commands
```bash
# Start database
./manage.sh start

# Stop database
./manage.sh stop

# Restart database
./manage.sh restart

# Show status
./manage.sh status

# View logs
./manage.sh logs
```

### Database Access
```bash
# Open PostgreSQL shell
./manage.sh shell

# Start with pgAdmin (web UI)
./manage.sh tools
# Then visit: http://localhost:8080
# Email: admin@chat.local, Password: admin123
```

### Backup & Restore
```bash
# Create backup
./manage.sh backup my_backup

# Restore from backup
./manage.sh restore backup_20240115_143022.sql.gz

# Reset database (WARNING: deletes all data)
./manage.sh reset
```

## 🗄️ Database Schema

### Messages Table (JSON Structure)
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message JSONB NOT NULL,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Message JSON Structure
The `message` field is a JSONB blob that can contain various fields:

**User Message Example:**
```json
{
  "role": "user",
  "content": "Hello, how are you?",
  "timestamp": "2024-01-15T10:30:00",
  "user_id": "user123",
  "session_id": "sess456",
  "lead": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Assistant Message Example:**
```json
{
  "role": "assistant", 
  "content": "I'm doing well, thank you!",
  "timestamp": "2024-01-15T10:30:05",
  "reference_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_to": 123,
  "model": "gpt-4",
  "tokens_used": 25,
  "response_time": 0.85,
  "confidence": 0.95
}
```

### Indexes
- `idx_messages_created_date` - Query by date
- `idx_messages_role` - GIN index on role field
- `idx_messages_content` - GIN index on content field  
- `idx_messages_role_date` - Combined role and date queries
- `idx_messages_message_id` - Index on message ID if present

### Database Functions
The database container only handles schema creation and basic setup. All query logic is implemented in the backend Python code for better maintainability and flexibility.

## 🔌 Backend Integration

### Connection String
```bash
# Default (Docker container)
DATABASE_URL=postgresql+psycopg://chatuser:chatpass@localhost:5432/chatdb

# Custom connection
DATABASE_URL=postgresql+psycopg://user:pass@host:port/database
```

### Backend Setup
1. Ensure database is running: `./manage.sh start`
2. Backend will automatically connect and load cache
3. No manual table creation needed (auto-initialized)

## 🐳 Docker Configuration

### Services
- **postgres**: Main database container
- **pgadmin**: Web-based database management (optional)

### Volumes
- `postgres_data`: Persistent database storage
- `pgadmin_data`: pgAdmin configuration

### Networks
- `chat-network`: Internal communication

### Health Checks
- PostgreSQL: `pg_isready` every 30 seconds
- Startup grace period: 40 seconds

## 🔒 Security

### Default Credentials
- **Database**: `chatdb`
- **User**: `chatuser`
- **Password**: `chatpass`

### Production Security
```bash
# Change default credentials in docker-compose.yml
environment:
  POSTGRES_DB: your_db_name
  POSTGRES_USER: your_username
  POSTGRES_PASSWORD: your_secure_password

# Update backend connection string accordingly
DATABASE_URL=postgresql+psycopg://your_username:your_secure_password@localhost:5432/your_db_name
```

## 🛠️ Advanced Usage

### Custom Initialization
Add SQL files to `scripts/init/` (they run in alphabetical order):
```bash
scripts/init/
├── 01-create-tables.sql    # Schema
├── 02-create-functions.sql # Functions
├── 03-your-custom.sql      # Your additions
```

### Environment Variables
```bash
# In docker-compose.yml
POSTGRES_DB=chatdb          # Database name
POSTGRES_USER=chatuser      # Database user
POSTGRES_PASSWORD=chatpass  # Database password
PGDATA=/var/lib/postgresql/data/pgdata  # Data directory
```

### Backup Automation
```bash
# Create daily backup cron job
0 2 * * * cd /path/to/database && ./manage.sh backup daily_$(date +\%Y\%m\%d)
```

## 🧪 Development

### Testing Connection
```bash
# Test from host
psql -h localhost -p 5432 -U chatuser -d chatdb

# Test from container
docker exec -it chat-postgres psql -U chatuser -d chatdb
```

### Development Data
The container includes sample messages for testing. Remove them in production by editing `01-create-tables.sql`.

## 🚀 Production Deployment

### Docker Compose Production
```yaml
# Override for production
services:
  postgres:
    restart: always
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    secrets:
      - postgres_password
    
secrets:
  postgres_password:
    file: ./postgres_password.txt
```

### Monitoring
```bash
# Monitor logs
docker-compose logs -f postgres

# Monitor performance
docker exec chat-postgres pg_stat_activity
```

## 🔧 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check Docker status
docker ps -a

# Check logs
docker-compose logs postgres

# Reset everything
docker-compose down -v && docker-compose up -d
```

**Connection refused:**
```bash
# Wait for health check
./manage.sh status

# Check port binding
docker port chat-postgres

# Test connection
telnet localhost 5432
```

**Permission denied:**
```bash
# Fix script permissions
chmod +x manage.sh scripts/*.sh

# Check Docker permissions
docker run --rm -v $(pwd):/test alpine ls -la /test
```

The database is now completely **decoupled** from the backend and can be managed independently! 🎉
