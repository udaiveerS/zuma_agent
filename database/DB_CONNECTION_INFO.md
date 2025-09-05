# Database Connection Information

## Connection Details
- **Host:** localhost
- **Port:** 5432
- **Database:** chatdb
- **Username:** chatuser
- **Password:** chatpass

## Desktop Database Editors

### 1. **TablePlus** (Recommended for Mac)
- Download: https://tableplus.com/
- Beautiful, fast, native Mac app
- Great for viewing and editing data

### 2. **DBeaver** (Free, Cross-platform)
- Download: https://dbeaver.io/
- Free and powerful
- Works on Mac, Windows, Linux

### 3. **Postico** (Mac-only)
- Download: https://eggerapps.at/postico/
- Clean, simple PostgreSQL client

### 4. **pgAdmin** (Web-based)
- Run: `docker compose -f docker-compose.pgadmin.yml up -d`
- Access: http://localhost:5050
- Login: admin@example.com / admin123

## Connection String
```
postgresql://chatuser:chatpass@localhost:5432/chatdb
```

## Quick Test Query
```sql
SELECT id, role, message->>'content' as content, created_date 
FROM messages 
ORDER BY created_date DESC;
```
