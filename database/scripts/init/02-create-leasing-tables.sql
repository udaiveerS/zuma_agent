-- Migration: Add leasing MVP tables
-- This script creates the core tables for the property leasing system

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Communities table
CREATE TABLE IF NOT EXISTS communities (
    community_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier TEXT UNIQUE NOT NULL,  -- e.g. "sunset-ridge", "downtown-lofts"
    name TEXT NOT NULL,
    timezone TEXT
);

-- Users table (leads - no FK to communities)
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    preferences JSONB,  -- e.g. { "bedrooms": 2, "move_in": "2025-07-01", "pet_type": "cat" }
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Units table
CREATE TABLE IF NOT EXISTS units (
    unit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    community_id UUID NOT NULL REFERENCES communities(community_id) ON DELETE CASCADE,
    unit_code TEXT NOT NULL,  -- human code, unique per community
    bedrooms INT NOT NULL,
    bathrooms NUMERIC(3,1) NOT NULL,
    availability_status TEXT NOT NULL CHECK (availability_status IN ('available','notice','occupied','offline')),
    available_at TIMESTAMPTZ,  -- NULL means immediate
    rent NUMERIC(10,2) NOT NULL,
    specials JSONB,  -- list of promo objects (arbitrary JSON)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (community_id, unit_code)
);

-- Units indexes
CREATE INDEX IF NOT EXISTS units_search_idx ON units (community_id, bedrooms, availability_status, available_at);

-- Community policies table (keep one active row per community_id, policy_type)
CREATE TABLE IF NOT EXISTS community_policies (
    policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    community_id UUID NOT NULL REFERENCES communities(community_id) ON DELETE CASCADE,
    policy_type TEXT NOT NULL CHECK (policy_type IN ('pet','smoking','parking')),
    rules JSONB NOT NULL,  -- e.g. { "cat": {"allowed": true, "fee": 50}, "dog": {"allowed": false} }
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Community policies indexes
CREATE UNIQUE INDEX IF NOT EXISTS community_policies_active_uniq ON community_policies(community_id, policy_type);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    community_id UUID NOT NULL REFERENCES communities(community_id) ON DELETE CASCADE,
    unit_id UUID REFERENCES units(unit_id) ON DELETE SET NULL,  -- nullable for general tours
    booking_type TEXT NOT NULL CHECK (booking_type IN ('tour','hold')),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('tentative','confirmed','canceled')),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Bookings indexes
CREATE INDEX IF NOT EXISTS bookings_by_comm_time ON bookings (community_id, start_time);
CREATE INDEX IF NOT EXISTS bookings_by_unit_time ON bookings (unit_id, start_time);

-- Note: Leaving existing messages table unchanged

-- Insert sample data for testing
INSERT INTO communities (identifier, name, timezone) VALUES 
    ('sunset-ridge', 'Sunset Ridge Apartments', 'America/Los_Angeles'),
    ('downtown-lofts', 'Downtown Lofts', 'America/New_York')
ON CONFLICT DO NOTHING;

-- Add some community identifier comments for easier testing
-- Community identifiers that can be used:
-- "Sunset Ridge Apartments" or "sunset-ridge" -> Sunset Ridge Apartments
-- "Downtown Lofts" or "downtown-lofts" -> Downtown Lofts

-- Get community IDs for sample data
DO $$
DECLARE
    sunset_id UUID;
    downtown_id UUID;
BEGIN
    SELECT community_id INTO sunset_id FROM communities WHERE identifier = 'sunset-ridge';
    SELECT community_id INTO downtown_id FROM communities WHERE identifier = 'downtown-lofts';
    
    -- Insert sample units
    INSERT INTO units (community_id, unit_code, bedrooms, bathrooms, availability_status, available_at, rent, specials) VALUES 
        (sunset_id, 'A101', 1, 1.0, 'available', NULL, 1200.00, '[]'),
        (sunset_id, 'A102', 1, 1.0, 'occupied', NULL, 1200.00, '[]'),
        (sunset_id, 'A103', 1, 1.0, 'notice', '2025-08-01'::timestamptz, 1250.00, '[]'),
        (sunset_id, 'B201', 2, 2.0, 'available', NULL, 1800.00, '[{"type": "move_in", "description": "First month free", "value": 1800}]'),
        (sunset_id, 'B202', 2, 2.0, 'notice', '2025-07-15'::timestamptz, 1850.00, '[]'),
        (downtown_id, 'L301', 2, 2.0, 'available', NULL, 2500.00, '[]'),
        (downtown_id, 'L302', 2, 2.0, 'notice', '2025-09-01'::timestamptz, 2600.00, '[{"type": "early_lease", "description": "Sign early and save $200/month", "value": 200}]')
    ON CONFLICT DO NOTHING;
    
    -- Insert sample policies
    INSERT INTO community_policies (community_id, policy_type, rules) VALUES 
        (sunset_id, 'pet', '{"cat": {"allowed": true, "fee": 50, "deposit": 200}, "dog": {"allowed": true, "fee": 75, "deposit": 300, "weight_limit": 50}}'),
        (sunset_id, 'smoking', '{"allowed": false, "designated_areas": []}'),
        (downtown_id, 'pet', '{"cat": {"allowed": true, "fee": 100}, "dog": {"allowed": false}}')
    ON CONFLICT DO NOTHING;
END $$;
