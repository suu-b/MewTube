CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS videos (
    videoId uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    thumbnail_url TEXT NOT NULL,
    channel_id TEXT NOT NULL REFERENCES channels(videoId) ON DELETE CASCADE,
)