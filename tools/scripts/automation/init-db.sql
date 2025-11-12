-- Sentinela IAM Database Initialization Script
-- Version: 1.0.0
-- Created: 2025-11-12

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paused', 'archived')),
    environment VARCHAR(20) NOT NULL DEFAULT 'development' CHECK (environment IN ('development', 'staging', 'production')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID
);

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    key_prefix VARCHAR(10) NOT NULL DEFAULT 'app_',
    key_hash VARCHAR(255) NOT NULL,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_applications_slug ON applications(slug);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_api_keys_application_id ON api_keys(application_id);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for applications table
CREATE TRIGGER update_applications_updated_at BEFORE UPDATE
    ON applications FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert seed data for development
INSERT INTO applications (name, slug, description, status, environment) VALUES
    ('Sentinela Demo App', 'sentinela-demo', 'Demo application for testing Sentinela IAM', 'active', 'development'),
    ('My Blog Platform', 'my-blog', 'Personal blog platform with comment moderation', 'active', 'production'),
    ('Admin Dashboard', 'admin-dashboard', 'Internal admin dashboard for team', 'active', 'staging')
ON CONFLICT (slug) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sentinela;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sentinela;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Sentinela database initialized successfully!';
END $$;
