#!/bin/bash

# Database Integration Test Runner
# Run from the database directory: ./tests/run_tests.sh

echo "🔍 Running Database Integration Tests..."
echo "========================================"

# Check if database is running
if ! docker compose ps postgres | grep -q "Up"; then
    echo "❌ PostgreSQL container is not running!"
    echo "Start it with: docker compose up -d postgres"
    exit 1
fi

echo "✅ Database is running"
echo ""

# Run the integration tests
echo "📊 Executing integration test queries..."
docker compose exec -T postgres psql -U chatuser -d chatdb << 'EOF'

\echo '1) Communities with unit counts:'
SELECT 
    c.name,
    c.timezone,
    COUNT(u.unit_id) as unit_count
FROM communities c
LEFT JOIN units u ON c.community_id = u.community_id
GROUP BY c.community_id, c.name, c.timezone
ORDER BY c.name;

\echo ''
\echo '2) Available 2-bedroom units by immediacy:'
SELECT 
    c.name as community_name,
    u.unit_code,
    u.bedrooms,
    u.availability_status,
    CASE WHEN u.available_at IS NULL THEN 'Immediate' ELSE u.available_at::text END as availability
FROM communities c
JOIN units u ON c.community_id = u.community_id
WHERE u.bedrooms = 2 AND u.availability_status = 'available'
ORDER BY c.name, u.available_at NULLS FIRST;

\echo ''
\echo '3) Pet policies per community:'
SELECT 
    c.name as community_name,
    cp.rules->'cat'->>'allowed' as cats_allowed,
    cp.rules->'cat'->>'fee' as cat_fee,
    cp.rules->'dog'->>'allowed' as dogs_allowed,
    cp.rules->'dog'->>'fee' as dog_fee
FROM communities c
LEFT JOIN community_policies cp ON c.community_id = cp.community_id AND cp.policy_type = 'pet'
ORDER BY c.name;

\echo ''
\echo '6) Data hygiene check - past dates with wrong status:'
SELECT 
    c.name as community_name,
    u.unit_code,
    u.availability_status,
    u.available_at,
    'Data inconsistency: past date but not available' as issue
FROM units u
JOIN communities c ON u.community_id = c.community_id
WHERE u.available_at < CURRENT_DATE 
    AND u.availability_status != 'available';

\echo ''
\echo '7) Duplicate unit codes check (should be empty):'
SELECT 
    c.name as community_name,
    u.unit_code,
    COUNT(*) as duplicate_count
FROM units u
JOIN communities c ON u.community_id = c.community_id
GROUP BY c.community_id, c.name, u.unit_code
HAVING COUNT(*) > 1
ORDER BY c.name, u.unit_code;

\echo ''
\echo '8) Message visibility breakdown:'
SELECT 
    role,
    visible_to_user,
    COUNT(*) as message_count,
    CASE 
        WHEN visible_to_user = true THEN 'User-facing'
        ELSE 'Hidden/Tool'
    END as message_type
FROM messages
GROUP BY role, visible_to_user
ORDER BY role, visible_to_user DESC;

EOF

echo ""
echo "✅ Integration tests completed!"
echo "📋 Review the results above for any data issues."
