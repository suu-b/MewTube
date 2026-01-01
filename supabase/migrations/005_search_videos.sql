-- SQL function to run a similarity search against the videos on supabase
CREATE OR REPLACE FUNCTION search_videos(
    q vector(384),
    k int DEFAULT 50
)

-- What to return from the function
RETURNS TABLE (
    id text,
    similarity real,
    quality_score real,
    channel_score real
)

LANGUAGE sql 
STABLE

-- Kinda the function body
-- Ranks the rows on the base of cosine similarity score
AS $$
  SELECT
    v.id,
    1 - (v.embedding <=> q) AS similarity,
    v.quality_score,
    c.channel_score AS channel_score
  FROM videos v
  JOIN channels c ON v.channel_id = c.id
  ORDER BY v.embedding <=> q
  LIMIT k;
$$;
