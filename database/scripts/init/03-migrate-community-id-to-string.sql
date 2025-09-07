-- Migration: Change community_id from UUID to string identifier
-- This migration updates all tables to use string identifiers instead of UUIDs

-- Step 1: Add new string identifier columns to tables that reference communities
ALTER TABLE units ADD COLUMN IF NOT EXISTS community_identifier TEXT;
ALTER TABLE community_policies ADD COLUMN IF NOT EXISTS community_identifier TEXT;
ALTER TABLE bookings ADD COLUMN IF NOT EXISTS community_identifier TEXT;

-- Step 2: Populate the new identifier columns with data from communities table
UPDATE units 
SET community_identifier = c.identifier 
FROM communities c 
WHERE units.community_id = c.community_id;

UPDATE community_policies 
SET community_identifier = c.identifier 
FROM communities c 
WHERE community_policies.community_id = c.community_id;

UPDATE bookings 
SET community_identifier = c.identifier 
FROM communities c 
WHERE bookings.community_id = c.community_id;

-- Step 3: Drop old foreign key constraints
ALTER TABLE units DROP CONSTRAINT IF EXISTS units_community_id_fkey;
ALTER TABLE community_policies DROP CONSTRAINT IF EXISTS community_policies_community_id_fkey;
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_community_id_fkey;

-- Step 4: Drop old UUID columns
ALTER TABLE units DROP COLUMN IF EXISTS community_id;
ALTER TABLE community_policies DROP COLUMN IF EXISTS community_id;
ALTER TABLE bookings DROP COLUMN IF EXISTS community_id;

-- Step 5: Rename new columns to community_id
ALTER TABLE units RENAME COLUMN community_identifier TO community_id;
ALTER TABLE community_policies RENAME COLUMN community_identifier TO community_id;
ALTER TABLE bookings RENAME COLUMN community_identifier TO community_id;

-- Step 6: Add NOT NULL constraints
ALTER TABLE units ALTER COLUMN community_id SET NOT NULL;
ALTER TABLE community_policies ALTER COLUMN community_id SET NOT NULL;
ALTER TABLE bookings ALTER COLUMN community_id SET NOT NULL;

-- Step 7: Add new foreign key constraints referencing communities.identifier
ALTER TABLE units ADD CONSTRAINT units_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

ALTER TABLE community_policies ADD CONSTRAINT community_policies_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

ALTER TABLE bookings ADD CONSTRAINT bookings_community_id_fkey 
    FOREIGN KEY (community_id) REFERENCES communities(identifier) ON DELETE CASCADE;

-- Step 8: Recreate indexes with new column types
DROP INDEX IF EXISTS units_search_idx;
CREATE INDEX units_search_idx ON units (community_id, bedrooms, availability_status, available_at);

DROP INDEX IF EXISTS community_policies_active_uniq;
CREATE UNIQUE INDEX community_policies_active_uniq ON community_policies(community_id, policy_type);

-- Step 9: Update the communities table to make identifier the primary key
-- First, drop the old primary key
ALTER TABLE communities DROP CONSTRAINT IF EXISTS communities_pkey;

-- Make identifier the primary key
ALTER TABLE communities ADD CONSTRAINT communities_pkey PRIMARY KEY (identifier);

-- Keep community_id as a unique column for any legacy references
ALTER TABLE communities ADD CONSTRAINT communities_community_id_unique UNIQUE (community_id);

-- Add some comments for clarity
COMMENT ON COLUMN units.community_id IS 'String identifier referencing communities.identifier (e.g. sunset-ridge)';
COMMENT ON COLUMN community_policies.community_id IS 'String identifier referencing communities.identifier (e.g. sunset-ridge)';
COMMENT ON COLUMN bookings.community_id IS 'String identifier referencing communities.identifier (e.g. sunset-ridge)';
