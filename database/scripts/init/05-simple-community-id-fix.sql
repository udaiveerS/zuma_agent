-- Simple Migration: Make ALL community_id columns TEXT strings like "sunset-ridge"
-- No UUIDs anywhere, just clean string identifiers

-- Step 1: Drop all foreign key constraints
ALTER TABLE units DROP CONSTRAINT IF EXISTS units_community_id_fkey;
ALTER TABLE community_policies DROP CONSTRAINT IF EXISTS community_policies_community_id_fkey;
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_community_id_fkey;

-- Step 2: Drop old primary key constraints
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_pkey;
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_community_id_unique;
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_identifier_key;

-- Step 3: Fix communities table - make community_id the string identifier
ALTER TABLE communities DROP COLUMN IF EXISTS identifier;
ALTER TABLE communities ALTER COLUMN community_id TYPE TEXT;
ALTER TABLE communities ALTER COLUMN community_id DROP DEFAULT;

-- Update communities data to use string identifiers
UPDATE communities SET community_id = 'sunset-ridge' WHERE name = 'Sunset Ridge Apartments';
UPDATE communities SET community_id = 'downtown-lofts' WHERE name = 'Downtown Lofts';

-- Make community_id the primary key
ALTER TABLE communities ADD CONSTRAINT communities_pkey PRIMARY KEY (community_id);

-- Step 4: Fix all referencing tables to use TEXT
-- Units table
ALTER TABLE units ALTER COLUMN community_id TYPE TEXT;
UPDATE units SET community_id = 'sunset-ridge' WHERE community_id::text LIKE '%sunset%' OR community_id::text LIKE '%ridge%';
UPDATE units SET community_id = 'downtown-lofts' WHERE community_id::text LIKE '%downtown%' OR community_id::text LIKE '%loft%';

-- Community policies table  
ALTER TABLE community_policies ALTER COLUMN community_id TYPE TEXT;
UPDATE community_policies SET community_id = 'sunset-ridge' WHERE community_id::text LIKE '%sunset%' OR community_id::text LIKE '%ridge%';
UPDATE community_policies SET community_id = 'downtown-lofts' WHERE community_id::text LIKE '%downtown%' OR community_id::text LIKE '%loft%';

-- Bookings table
ALTER TABLE bookings ALTER COLUMN community_id TYPE TEXT;
UPDATE bookings SET community_id = 'sunset-ridge' WHERE community_id::text LIKE '%sunset%' OR community_id::text LIKE '%ridge%';
UPDATE bookings SET community_id = 'downtown-lofts' WHERE community_id::text LIKE '%downtown%' OR community_id::text LIKE '%loft%';

-- Step 5: Add back foreign key constraints
ALTER TABLE units ADD CONSTRAINT units_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(community_id) ON DELETE CASCADE;

ALTER TABLE community_policies ADD CONSTRAINT community_policies_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(community_id) ON DELETE CASCADE;

ALTER TABLE bookings ADD CONSTRAINT bookings_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(community_id) ON DELETE CASCADE;

-- Step 6: Recreate indexes
DROP INDEX IF EXISTS units_search_idx;
CREATE INDEX units_search_idx ON units (community_id, bedrooms, availability_status, available_at);

DROP INDEX IF EXISTS community_policies_active_uniq;
CREATE UNIQUE INDEX community_policies_active_uniq ON community_policies(community_id, policy_type);

-- Verify the results
SELECT 'Final verification:' as status;
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE column_name = 'community_id' 
ORDER BY table_name;

SELECT 'Sample data:' as status;
SELECT community_id, name FROM communities;
SELECT community_id, policy_type FROM community_policies;
SELECT community_id, unit_code FROM units LIMIT 3;
