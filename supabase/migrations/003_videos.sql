CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS videos (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMPTZ NOT NULL,
    thumbnail_url TEXT NOT NULL,
    channel_id uuid NOT NULL REFERENCES channels(id) ON DELETE CASCADE,

    embedding vector(384) NOT NULL,
    quality_score NUMERIC(3,2) NOT NULL
        CHECK (quality_score >= 0.0 AND quality_score <= 1.0)
);

-- An index on the embeddings. It will let vector lib to divide the videos among clusters. Our query will be matched against the centroids and then the cluster of the nearest centroid.
CREATE INDEX videos_embedding_idx
ON videos
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
