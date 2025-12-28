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
YT_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
YT_PLAYLIST_ITEMS_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

YT_KEY = os.getenv("YT_KEY")
OUTPUT = Path(__file__).resolve().parents[0]
OUTPUT_DR = OUTPUT / "output"
OUTPUT_DR.mkdir(exist_ok=True)

layer1 = OUTPUT_DR / "layer1.jsonl"
layer2 = OUTPUT_DR / "layer2.jsonl"
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
    params = {
        "forHandle": "unsolicitedadvice9198",
        "part": "snippet,contentDetails",
        "key": YT_KEY,
        "regionCode": "US",
    }

    r = requests.get(YT_CHANNELS_URL, params=params, timeout=10)
    if r.status_code != 200:
            logger.error(
                "YouTube API call failed",
                extra={
                    "status_code": r.status_code,
                    "response": r.text,
                },
            )
            raise HTTPException(r.status_code, r.text)
    # logger.info(r.json())
    data = r.json().get("items", [])
    channel_data = validate(data[0])
    # logger.info(channel_data)
    with open(layer1, "a", encoding="utf-8") as f:
        f.write(json.dumps(channel_data.model_dump(mode = "json"), ensure_ascii=False) + "\n")
    
    upload_playlist_id = channel_data.upload_playlist_id
    # logger.info(upload_playlist_id)
    # return
    params_playlist = {
        "playlistId": upload_playlist_id,
        "part": "snippet,contentDetails",
        "key": YT_KEY,
        "regionCode": "US",
        "maxResults": 50
    }
    next_page_token = ""
    playlist_data = []

    r_playlist = requests.get(YT_PLAYLIST_ITEMS_URL, params=params_playlist, timeout=10)
    if r_playlist.status_code != 200:
        logger.error(
            "YouTube API call failed for playlists",
            extra={
                "status_code": r.status_code,
                "response": r.text,
            },
        )
        raise HTTPException(r.status_code, r.text)
    playlist_data += r_playlist.json().get("items", [])
    next_page_token = r_playlist.json().get("nextPageToken", "")
    
    while next_page_token != "":
        logger.info(next_page_token)
        params_playlist["pageToken"] = next_page_token
        r_playlist = requests.get(YT_PLAYLIST_ITEMS_URL, params=params_playlist, timeout=10)
        if r_playlist.status_code != 200:
            logger.error(
                "YouTube API call failed for playlists",
                extra={
                    "status_code": r.status_code,
                    "response": r.text,
                },
            )
            raise HTTPException(r.status_code, r.text)
        playlist_data += r_playlist.json().get("items", [])
        next_page_token = r_playlist.json().get("nextPageToken", "")

    # return
    validated_playlist_data = [validate_playlist_data(d) for d in playlist_data]

    with open(OUTPUT_DR / f"{upload_playlist_id}.json", "a", encoding="utf-8") as f:
        json.dump(
            [d.model_dump(mode="json") for d in validated_playlist_data],
            f,
            indent=2,
            ensure_ascii=False
        ) 

if __name__ == "__main__":
    main()
