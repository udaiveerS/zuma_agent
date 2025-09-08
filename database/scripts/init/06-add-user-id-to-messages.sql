-- Migration: Add user_id to messages table for user tracking
-- This links messages to users for proper user context and preferences

-- Add user_id column to messages table
ALTER TABLE messages 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(user_id) ON DELETE SET NULL;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO chatuser;
