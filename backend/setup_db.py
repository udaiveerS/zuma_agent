#!/usr/bin/env python3
"""
Database connection test script.
Tests the connection to the PostgreSQL container.
"""

from db import get_db, engine
from sqlalchemy import text

def test_database():
    """Test database connection and show basic info"""
    print("🔍 Testing database connection...")
    try:
        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL!")
            print(f"📊 Version: {version}")
            
        # Test table existence
        db = next(get_db())
        try:
            result = db.execute(text("SELECT COUNT(*) FROM messages"))
            count = result.fetchone()[0]
            print(f"📋 Messages table exists with {count} records")
        except Exception as e:
            print(f"⚠️  Messages table not found: {e}")
            print("💡 Make sure the database container is initialized")
        finally:
            db.close()
            
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure the database container is running:")
        print("   cd database && ./manage.sh start")
        return False

if __name__ == "__main__":
    test_database()
