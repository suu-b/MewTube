import subprocess
from pathlib import Path
from config.config import logger
import requests
from config.config import logger
from dotenv import load_dotenv 
import os
from http.client import HTTPException
from pathlib import Path
import json
from datetime import datetime
from pydantic import BaseModel
load_dotenv()

pattern = "@[a-zA-Z0-9_-]+"

OUTPUT = Path(__file__).resolve().parents[0]
OUTPUT_DR = OUTPUT / "output"
OUTPUT_DR.mkdir(exist_ok=True)

YT_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"

YT_KEY = os.getenv("YT_KEY")

layer3 = OUTPUT_DR / "layer3.jsonl"


class Channel(BaseModel):
    channel_id: str
    title: str
    description: str
    handle: str

    upload_playlist_id: str

class PlaylistVideo(BaseModel):
    video_id: str
    title: str
    description: str | None = None

    channel_id: str
    channel_title: str

    published_at: datetime

    thumbnail_url: str

def validate(result) -> Channel:
    snippet = result["snippet"]
    contentDetails = result["contentDetails"]

    return Channel(
        channel_id=result["id"],
        title=snippet["title"],
        description=snippet.get("description"),
        handle=snippet.get("customUrl"),
        upload_playlist_id=contentDetails["relatedPlaylists"]["uploads"]
    )

def validate_playlist_data(result) -> PlaylistVideo:
    snippet = result["snippet"]
    return PlaylistVideo(
        video_id=result["id"],
        title=snippet["title"],
        description=snippet.get("description"),
        channel_id=snippet["channelId"],
        channel_title=snippet["channelTitle"],
        published_at=snippet["publishedAt"],
        fetched_at=datetime.utcnow(),
        thumbnail_url=snippet["thumbnails"]["medium"]["url"],
    )

def main():
    channels = []
    with open(OUTPUT_DR / "layer2.jsonl", "r", encoding="utf-8") as f:
        channels = [Channel.model_validate_json(line) for line in f]

    for channel in channels:
        logger.info("Channel: %s", channel.title)
        result = subprocess.run(
            ['grep', '-oE', pattern, f"/home/suub/IdeaProjects/MewTube/neo/output/{channel.upload_playlist_id}.json"],
            capture_output=True,
            text=True
        )    
        search_results = {s for s in result.stdout.splitlines() if s and not s.endswith('gmail')}

        for handle in search_results:
            params = {
                "forHandle": handle,
                "part": "snippet,contentDetails",
                "key": YT_KEY,
                "regionCode": "US",
            }

            r = requests.get(YT_CHANNELS_URL, params=params, timeout=10)
            if r.status_code != 200:
                logger.error(
                    "YouTube API call for channel failed",
                    extra={
                        "status_code": r.status_code,
                        "response": r.text,
                    },
                )
                raise HTTPException(r.status_code, r.text)
            # logger.info(r.json())
            data = r.json().get("items", [])
            if not data:
                logger.warning("Empty data for %s", handle)
                continue

            channel_data = validate(data[0])
            # logger.info(channel_data)
            with open(layer3, "a", encoding="utf-8") as f:
                f.write(json.dumps(channel_data.model_dump(mode = "json"), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()