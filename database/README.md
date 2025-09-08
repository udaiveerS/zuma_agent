# Database

Containerized PostgreSQL database for the Chat API application.

## Quick Start

```bash
# Start database
docker compose up -d

# Check status  
docker compose ps

# View logs
docker compose logs postgres
```

## Connection

The backend connects automatically using environment variables from `.env` files.

**Database**: `chatdb`  
**Port**: `5432`  
**Credentials**: Set in your local `.env` files (not in version control)

## Management

```bash
# Stop database
docker compose down

# Reset database (WARNING: deletes all data)
docker compose down -v && docker compose up -d

# Database shell
docker exec -it chat-postgres psql -U chatuser -d chatdb
```

## Schema

**Core Tables:**
- **messages**: Chat messages with JSONB structure (id, message, role, visible_to_user, step_id, parent_id, created_date)
- **communities**: Property locations (community_id, identifier, name, timezone)
- **units**: Rental units (unit_id, community_id, unit_code, bedrooms, bathrooms, availability_status, available_at, rent, specials)
- **community_policies**: Pet/smoking/parking rules stored as JSONB (policy_id, community_id, policy_type, rules)
- **users**: Lead information with preferences as JSONB (user_id, email, name, preferences)
- **bookings**: Tour scheduling (booking_id, community_id, unit_id, booking_type, start_time, end_time, status, user_id)

**Auto-initialization**: All tables created on first startup via SQL scripts in `scripts/init/`

## Production

- Change default credentials in `docker-compose.yml`
- Use Docker secrets for sensitive data
- Enable backups and monitoring
- Use external volumes for data persistence

See `docker-compose.yml` and initialization scripts in `scripts/init/` for details.