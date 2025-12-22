-- Installs pgcrypto extension for extra crypto functions like gen_random_uuid(). It is enabled by default in supabase but here just in case any other client doesn't have one
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Creates table for the model versioning
CREATE TABLE IF NOT EXISTS model_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    storage_bucket TEXT NOT NULL DEFAULT 'models',
    storage_path TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN ('active', 'shadow', 'deprecated')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (model_name, version)
);

-- Enforces that any model version has only and only one active model which our services can access
CREATE UNIQUE INDEX IF NOT EXISTS one_active_model
ON model_versions (model_name)
WHERE status = 'active';
