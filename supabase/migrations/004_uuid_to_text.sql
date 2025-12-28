-- We made a mistake by setting the type of the ids to be uuid as the ids will be yt provided ids.
-- We aim to alter their typing to text with a proper procedure by not obliterating existing data

ALTER TABLE videos 
  DROP CONSTRAINT IF EXISTS videos_channel_id_fkey;

ALTER TABLE videos 
  ALTER COLUMN id TYPE TEXT USING id::TEXT,
  ALTER COLUMN channel_id TYPE TEXT USING channel_id::TEXT;

ALTER TABLE channels
  ALTER COLUMN id TYPE TEXT USING id::TEXT;

ALTER TABLE videos
  ADD CONSTRAINT videos_channel_id_fkey
  FOREIGN KEY(channel_id) REFERENCES channels(id) ON DELETE CASCADE;