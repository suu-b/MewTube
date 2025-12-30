#!/usr/bin/env sh

# The script cleans and converts json video dumps to jsonl
mkdir -p mapped

for f in UU*.json; do
  jq -c '.[] | {id: .video_id, title: .title, description: .description, published_at: .published_at, thumbnail_url: .thumbnail_url, channel_id: .channel_id}' \
    "$f" > "mapped/${f%.json}.jsonl"
done
