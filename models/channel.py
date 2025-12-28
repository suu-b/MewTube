from pydantic import BaseModel, Field
from typing import Optional

class Channel(BaseModel):
    id: str
    title: str
    description: Optional[str]
    handle: str
    playlist_id: str
    channel_score: int = Field(..., ge=1, le=100)
