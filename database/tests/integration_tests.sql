-- Database Integration Test Queries
-- Run these queries to verify seed data behaves as intended

-- 1) List all communities with unit counts
SELECT 
    c.name,
    c.timezone,
    COUNT(u.unit_id) as unit_count
FROM communities c
LEFT JOIN units u ON c.community_id = u.community_id
GROUP BY c.community_id, c.name, c.timezone
ORDER BY c.name;

-- 2) For each community, list available 2-bedroom units ordered by immediacy (available_at NULL first)
SELECT 
    c.name as community_name,
    u.unit_code,
    u.bedrooms,
    u.availability_status,
    u.available_at,
    CASE WHEN u.available_at IS NULL THEN 'Immediate' ELSE u.available_at::text END as availability
FROM communities c
JOIN units u ON c.community_id = u.community_id
WHERE u.bedrooms = 2 AND u.availability_status = 'available'
ORDER BY c.name, u.available_at NULLS FIRST;

-- 3) Fetch pet policy JSON for 'cat' and 'dog' per community (show allowed + fee)
SELECT 
    c.name as community_name,
    cp.rules->'cat'->>'allowed' as cats_allowed,
    cp.rules->'cat'->>'fee' as cat_fee,
    cp.rules->'dog'->>'allowed' as dogs_allowed,
    cp.rules->'dog'->>'fee' as dog_fee
FROM communities c
LEFT JOIN community_policies cp ON c.community_id = cp.community_id AND cp.policy_type = 'pet'
ORDER BY c.name;

-- 4) For a given community_id, show next 3 tour bookings (start_time ASC)
-- Replace :community_id with actual community ID
SELECT 
    b.booking_id,
    b.start_time,
    b.end_time,
    b.status,
    u.unit_code
FROM bookings b
LEFT JOIN units u ON b.unit_id = u.unit_id
WHERE b.community_id = :community_id
    AND b.booking_type = 'tour'
    AND b.start_time > NOW()
    AND b.status != 'canceled'
ORDER BY b.start_time ASC
LIMIT 3;

-- 5) For a given unit_code + community, show rent and specials JSON
-- Replace :unit_code and :community_name with actual values
SELECT 
    c.name as community_name,
    u.unit_code,
    u.bedrooms,
    u.bathrooms,
    u.rent,
    u.specials
FROM units u
JOIN communities c ON u.community_id = c.community_id
WHERE u.unit_code = :unit_code 
    AND c.name = :community_name;

-- 6) Find any units whose available_at is in the past but status not 'available' (data hygiene)
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

-- 7) Find duplicate unit_code within same community (should be none)
SELECT 
    c.name as community_name,
    u.unit_code,
    COUNT(*) as duplicate_count
FROM units u
JOIN communities c ON u.community_id = c.community_id
GROUP BY c.community_id, c.name, u.unit_code
HAVING COUNT(*) > 1
ORDER BY c.name, u.unit_code;

-- 8) Count visible user-facing messages vs hidden tool messages (role/kind) for observability
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
