# Database Integration Tests

This folder contains SQL queries to verify seed data and database integrity.

## Running the Tests

### Option 1: Run all queries at once
```bash
# From the database directory
docker compose exec postgres psql -U chatuser -d chatdb -f /tests/integration_tests.sql
```

### Option 2: Run individual queries
```bash
# Connect to database
docker compose exec postgres psql -U chatuser -d chatdb

# Then copy/paste individual queries
```

### Option 3: Run with parameters
For queries with parameters (like `:community_id`), replace the placeholders:

```sql
-- Example: Replace :community_id with actual ID
SELECT * FROM tour_bookings tb
JOIN units u ON tb.unit_id = u.id
WHERE u.community_id = 1  -- Replace with actual community ID
```

## Test Categories

1. **Data Completeness**: Queries 1-3 verify basic data structure
2. **Business Logic**: Queries 4-5 test specific use cases
3. **Data Quality**: Queries 6-7 check for data inconsistencies
4. **System Health**: Query 8 provides observability metrics

## Expected Results

- **No duplicates** in query 7
- **No data hygiene issues** in query 6
- **Reasonable distribution** of visible vs hidden messages in query 8
- **Valid JSON structures** in pet policy and specials queries
