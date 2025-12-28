CREATE TABLE IF NOT EXISTS channels (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    handle TEXT NOT NULL UNIQUE,
    playlist_id TEXT NOT NULL,
    channel_score SMALLINT NOT NULL
        CHECK (channel_score BETWEEN 1 AND 100)
);

-- Handy to fetch channels with range
CREATE INDEX channels_score_idx ON channels (channel_score);
