from pydantic import BaseModel

class Top10Request(BaseModel):
    query: str