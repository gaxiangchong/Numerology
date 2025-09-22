-- Add has_default_password column to User table
-- Run this in PythonAnywhere console

-- Check if column exists first
PRAGMA table_info(user);

-- Add the column if it doesn't exist
ALTER TABLE user ADD COLUMN has_default_password BOOLEAN DEFAULT 0;

-- Update existing users
UPDATE user SET has_default_password = 0 WHERE has_default_password IS NULL;

-- Verify the column was added
PRAGMA table_info(user);

-- Show user count
SELECT COUNT(*) as total_users FROM user;
SELECT COUNT(*) as users_with_default_password FROM user WHERE has_default_password = 1;
