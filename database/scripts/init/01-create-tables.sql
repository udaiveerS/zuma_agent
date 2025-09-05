-- Chat API Database Initialization Script
-- This script creates the necessary tables for the chat application

-- Create messages table with new schema
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message JSONB NOT NULL,
    role VARCHAR(20) NOT NULL,
    visible_to_user BOOLEAN DEFAULT TRUE NOT NULL,
    step_id VARCHAR(20),
    parent_id UUID,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_messages_created_date ON messages(created_date);
CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);
CREATE INDEX IF NOT EXISTS idx_messages_visible_to_user ON messages(visible_to_user);
CREATE INDEX IF NOT EXISTS idx_messages_step_id ON messages(step_id);
CREATE INDEX IF NOT EXISTS idx_messages_parent_id ON messages(parent_id);
CREATE INDEX IF NOT EXISTS idx_messages_role_date ON messages(role, created_date);

-- Create GIN index for JSONB content search
CREATE INDEX IF NOT EXISTS idx_messages_content ON messages USING GIN ((message->>'content'));

-- Insert sample data (optional - remove in production)
INSERT INTO messages (message, role, created_date) VALUES 
    ('{"role": "assistant", "content": "Hello! I''m your AI assistant. How can I help you today?"}', 'assistant', NOW() - INTERVAL '1 hour'),
    ('{"role": "user", "content": "Hi there! Can you help me understand how this chat system works?"}', 'user', NOW() - INTERVAL '59 minutes'),
    ('{"role": "assistant", "content": "Of course! This is a chat system built with FastAPI and PostgreSQL. You can ask me questions and I''ll respond with helpful information."}', 'assistant', NOW() - INTERVAL '58 minutes')
ON CONFLICT DO NOTHING;

-- Grant permissions to the chat user
GRANT SELECT, INSERT, UPDATE, DELETE ON messages TO chatuser;
GRANT USAGE, SELECT ON SEQUENCE messages_id_seq TO chatuser;
