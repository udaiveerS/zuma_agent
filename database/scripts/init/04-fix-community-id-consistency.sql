-- Migration: Fix community_id consistency - make ALL community_id columns use string identifiers
-- This migration ensures all tables consistently use string identifiers, not UUIDs

-- Step 1: Drop all existing foreign key constraints that reference communities
ALTER TABLE units DROP CONSTRAINT IF EXISTS units_community_id_fkey;
ALTER TABLE community_policies DROP CONSTRAINT IF EXISTS community_policies_community_id_fkey;
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_community_id_fkey;

-- Step 2: Update the communities table structure
-- Drop the old primary key and make identifier the primary key
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_pkey;
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_community_id_unique;

-- Make identifier the primary key
ALTER TABLE communities ADD CONSTRAINT communities_pkey PRIMARY KEY (identifier);

-- Keep the UUID column but it's no longer the primary key
ALTER TABLE communities ADD CONSTRAINT communities_community_id_unique UNIQUE (community_id);

-- Step 3: Ensure all referencing tables use string identifiers
-- Check if any tables still have UUID community_id columns and fix them

-- For units table - should already be string from previous migration, but let's verify
DO $$
BEGIN
    -- Check if units.community_id is still UUID type
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'units' 
        AND column_name = 'community_id' 
        AND data_type = 'uuid'
    ) THEN
        -- If it's still UUID, we need to fix it
        ALTER TABLE units ADD COLUMN community_id_temp TEXT;
        
        UPDATE units 
        SET community_id_temp = c.identifier 
        FROM communities c 
        WHERE units.community_id = c.community_id;
        
        ALTER TABLE units DROP COLUMN community_id;
        ALTER TABLE units RENAME COLUMN community_id_temp TO community_id;
        ALTER TABLE units ALTER COLUMN community_id SET NOT NULL;
    END IF;
END $$;

-- For community_policies table
DO $$
BEGIN
    -- Check if community_policies.community_id is still UUID type
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'community_policies' 
        AND column_name = 'community_id' 
        AND data_type = 'uuid'
    ) THEN
        -- If it's still UUID, we need to fix it
        ALTER TABLE community_policies ADD COLUMN community_id_temp TEXT;
        
        UPDATE community_policies 
        SET community_id_temp = c.identifier 
        FROM communities c 
        WHERE community_policies.community_id = c.community_id;
        
        ALTER TABLE community_policies DROP COLUMN community_id;
        ALTER TABLE community_policies RENAME COLUMN community_id_temp TO community_id;
        ALTER TABLE community_policies ALTER COLUMN community_id SET NOT NULL;
    END IF;
END $$;

-- For bookings table
DO $$
BEGIN
    -- Check if bookings.community_id is still UUID type
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'bookings' 
        AND column_name = 'community_id' 
        AND data_type = 'uuid'
    ) THEN
        -- If it's still UUID, we need to fix it
        ALTER TABLE bookings ADD COLUMN community_id_temp TEXT;
        
        UPDATE bookings 
        SET community_id_temp = c.identifier 
        FROM communities c 
        WHERE bookings.community_id = c.community_id;
        
        ALTER TABLE bookings DROP COLUMN community_id;
        ALTER TABLE bookings RENAME COLUMN community_id_temp TO community_id;
        ALTER TABLE bookings ALTER COLUMN community_id SET NOT NULL;
    END IF;
END $$;

-- Step 4: Re-add foreign key constraints with string references
ALTER TABLE units ADD CONSTRAINT units_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

ALTER TABLE community_policies ADD CONSTRAINT community_policies_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

ALTER TABLE bookings ADD CONSTRAINT bookings_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

-- Step 5: Recreate indexes
DROP INDEX IF EXISTS units_search_idx;
CREATE INDEX units_search_idx ON units (community_id, bedrooms, availability_status, available_at);

DROP INDEX IF EXISTS community_policies_active_uniq;
CREATE UNIQUE INDEX community_policies_active_uniq ON community_policies(community_id, policy_type);

-- Step 6: Add helpful comments
COMMENT ON COLUMN communities.identifier IS 'Primary key - string identifier (e.g. sunset-ridge, downtown-lofts)';
COMMENT ON COLUMN communities.community_id IS 'Legacy UUID - kept for compatibility but no longer primary key';
COMMENT ON COLUMN units.community_id IS 'String identifier referencing communities.identifier';
COMMENT ON COLUMN community_policies.community_id IS 'String identifier referencing communities.identifier';
COMMENT ON COLUMN bookings.community_id IS 'String identifier referencing communities.identifier';

-- Step 7: Verify the changes
SELECT 'communities table structure:' as info;
\d communities;

SELECT 'Sample data verification:' as info;
SELECT 
    'communities' as table_name,
    identifier as community_id,
    name,
    pg_typeof(identifier) as id_type
FROM communities LIMIT 2;

SELECT 
    'units' as table_name,
    community_id,
    unit_code,
    pg_typeof(community_id) as id_type
FROM units LIMIT 2;

SELECT 
    'community_policies' as table_name,
    community_id,
    policy_type,
    pg_typeof(community_id) as id_type
FROM community_policies LIMIT 2;
