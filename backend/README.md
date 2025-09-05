# Chat API Backend

FastAPI backend for the chat application with PostgreSQL database and in-memory caching.

## 🏗️ Architecture

- **Package Manager**: `uv` (fast Python package installer)
- **Database**: PostgreSQL (persistent storage)
- **Cache**: In-process memory cache (fast access for message history)
- **Flow**: Database → Cache → API responses

## 🚀 Quick Setup with uv

### Option 1: Automated Setup
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run automated setup
uv run python scripts/setup.py
```

### Option 2: Manual Setup

### 1. Install uv
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

### 2. Install Dependencies
```bash
# Install all dependencies with uv
uv sync
```

### 3. Database Setup
```bash
# Install PostgreSQL (if not already installed)
brew install postgresql  # macOS
# sudo apt-get install postgresql  # Ubuntu

# Create database
createdb chatdb

# Create user (optional)
createuser -P chatuser  # Enter password when prompted
```

### 4. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env with your database credentials
# Example:
# DATABASE_URL=postgresql+psycopg://chatuser:password@localhost:5432/chatdb
```

### 5. Initialize Database Tables
```bash
# Run this ONCE to create tables
uv run python setup_db.py
```

### 6. Start the Server
```bash
# Development mode (recommended)
uv run python scripts/dev.py

# Or manually
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or direct python
uv run python app.py
```

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Health check |
| `POST` | `/api/reply` | Main chat endpoint |
| `GET` | `/api/messages` | Get message history (from cache) |
| `GET` | `/api/messages/db` | Get messages from database (admin) |
| `GET` | `/api/cache/status` | Cache status and preview |

## 🔄 Data Flow

1. **POST /api/reply**:
   - Save user message to database
   - Generate assistant response
   - Save assistant message to database
   - Add both messages to cache
   - Return assistant message

2. **GET /api/messages**:
   - Return message history from cache (fast)
   - Cache is loaded from database on startup

## 🗄️ Database Schema

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🧪 Testing

Visit http://localhost:8000/docs for interactive API documentation.

## 🔧 uv Commands Reference

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Run commands in virtual environment
uv run python script.py
uv run uvicorn app:app --reload

# Update dependencies
uv sync --upgrade

# Show project info
uv tree

# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8 .

# Run tests
uv run pytest
```

## 📁 Project Structure with uv

```
backend/
├── pyproject.toml       # uv project configuration (replaces requirements.txt)
├── uv.lock             # Lock file (auto-generated, like package-lock.json)
├── .venv/              # Virtual environment (auto-created by uv)
├── scripts/
│   ├── dev.py          # Development server script
│   └── setup.py        # Automated setup script
├── app.py              # FastAPI application
├── db.py               # Database configuration
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── cache.py            # In-memory cache
├── setup_db.py         # Database setup script
├── env.example         # Environment template
└── README.md           # This file
```

## 🚀 Production Notes

- The database is persistent - tables are NOT recreated on startup
- Cache is rebuilt from database on each server restart
- Use proper PostgreSQL credentials in production
- Consider adding database connection pooling for high traffic
- `uv` provides faster dependency resolution and installation
- Virtual environment is automatically managed by `uv`
