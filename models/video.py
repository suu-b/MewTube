from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional, List

class Video(BaseModel):
    id: str
    title: str
    description: Optional[str]
    published_at: datetime
    thumbnail_url: str
    channel_id: str
    embedding: List[float] 
    quality_score: condecimal(ge=0, le=1, max_digits=3, decimal_places=2)
