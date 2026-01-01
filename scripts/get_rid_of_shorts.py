import requests
import os
import isodate
import time

from dotenv import load_dotenv
from supabase import create_client

from models.video import Video
from config.config import OUTPUT_DIR, VIDEO_TABLE, logger
from util import decode_video_id

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
YT_KEY = os.getenv('YT_KEY')

client = create_client(SUPABASE_URL, SUPABASE_KEY)

BATCH_SIZE_SUPABASE = 500  
BATCH_SIZE_YT = 50       

def fetch_youtube_info(video_ids: list) -> list:
    results = []
    for i in range(0, len(video_ids), BATCH_SIZE_YT):
        batch = video_ids[i:i+BATCH_SIZE_YT]
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "contentDetails,snippet",
            "id": ",".join(batch),
            "key": YT_KEY
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        results.extend(resp.json().get("items", []))
        time.sleep(0.1) 
    return results

def main():
    logger.info("Getting rid of shorts...")
    offset = 0
    while True:
        data = client.table(VIDEO_TABLE).select("id").range(offset, offset + BATCH_SIZE_SUPABASE - 1).execute()
        rows = data.data
        if not rows:
            break

        encoded_ids = [row["id"] for row in rows]
        video_ids = [decode_video_id(eid) for eid in encoded_ids]

        videos_info = fetch_youtube_info(video_ids)

        yt_info_map = {v["id"]: v for v in videos_info}
        short_video_ids = [
            eid for eid, vid in zip(encoded_ids, video_ids)
            if vid in yt_info_map and isodate.parse_duration(yt_info_map[vid]["contentDetails"]["duration"]).total_seconds() < 61
        ]

        if short_video_ids:
            client.table(VIDEO_TABLE).delete().in_("id", short_video_ids).execute()
            logger.info(f"Deleted {len(short_video_ids)} short videos in this batch.")

        offset += BATCH_SIZE_SUPABASE

    logger.info("Got rid %d shorts. Hush!", len(short_video_ids))

if __name__ == "__main__":
    main()
