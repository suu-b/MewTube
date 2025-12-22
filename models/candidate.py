from pydantic import BaseModel
from datetime import datetime

class Candidate(BaseModel):
    video_id: str
    title: str
    description: str | None = None

    channel_id: str
    channel_title: str

    published_at: datetime
    fetched_at: datetime

    thumbnail_url: str