"""
Global Database Configuration

Database session management with per-request sessions.
Uses eager initialization pattern - connection pool created at startup.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables. Please set it in your .env file.")

# Eager initialization - created at import time for connection pooling
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency to get database session.
    Creates a new session for each request, ensures proper cleanup.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Table creation is handled by Docker container initialization
# See database/scripts/init/ for schema management
