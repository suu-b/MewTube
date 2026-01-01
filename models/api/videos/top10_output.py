from pydantic import BaseModel, condecimal, Field, field_validator
from util import decode_video_id

class Top10Output(BaseModel):
    id: str
    similarity: condecimal()
    quality_score: condecimal(ge=0, le=1, max_digits=3, decimal_places=2)
    channel_score: int = Field(..., ge=1, le=100)

    @field_validator("id", mode="before")
    @classmethod
    def decode_id(cls, v):
        return decode_video_id(v)