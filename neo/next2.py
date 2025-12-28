import subprocess
from pathlib import Path

from altair.vegalite.v6.schema.channels import ChannelShape
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
path = "/home/suub/IdeaProjects/MewTube/neo/output/UUW71hQg1kDxmFIfijA8dL0Q.json"

OUTPUT = Path(__file__).resolve().parents[0]
OUTPUT_DR = OUTPUT / "output"
OUTPUT_DR.mkdir(exist_ok=True)

YT_PLAYLIST_ITEMS_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

YT_KEY = os.getenv("YT_KEY")


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

    logger.info("Total channels read: %d", len(channels))
    if not channels:
        logger.warning("No channel found. Exiting...")
        return

    for channel in channels:
        logger.info("Channel: %s", channel.title)
        playlist_data = []
        next_page_token = ""
        params_playlist = {
            "playlistId": channel.upload_playlist_id,
            "part": "snippet,contentDetails",
            "key": YT_KEY,
            "regionCode": "US",
            "maxResults": 50
        }
        r_playlist = requests.get(YT_PLAYLIST_ITEMS_URL, params=params_playlist, timeout=10)
        if r_playlist.status_code != 200:
            logger.error(
                "YouTube API call failed for playlists",
                extra={
                    "status_code": r_playlist.status_code,
                    "response": r_playlist.text,
                },
            )
            raise HTTPException(r_playlist.status_code, r_playlist.text)
        playlist_data += r_playlist.json().get("items", [])
        next_page_token = r_playlist.json().get("nextPageToken", "")

        while next_page_token != "":
            logger.info("Page Token: %s", next_page_token)
            params_playlist["pageToken"] = next_page_token
            r_playlist = requests.get(YT_PLAYLIST_ITEMS_URL, params=params_playlist, timeout=10)
            if r_playlist.status_code != 200:
                logger.error(
                    "YouTube API call failed for playlists",
                    extra={
                        "status_code": r_playlist.status_code,
                        "response": r_playlist.text,
                    },
                )
                raise HTTPException(r_playlist.status_code, r_playlist.text)
            playlist_data += r_playlist.json().get("items", [])
            next_page_token = r_playlist.json().get("nextPageToken", "")

        #return
        validated_playlist_data = [validate_playlist_data(d) for d in playlist_data]
        with open(OUTPUT_DR / f"{channel.upload_playlist_id}.json", "a", encoding="utf-8") as f:
             json.dump(
                [d.model_dump(mode="json") for d in validated_playlist_data],
                f,
                indent=2,
                ensure_ascii=False
            ) 


if __name__ == "__main__":
    main()