from pydantic import BaseModel
from typing import List

from models.api.videos.top10_output import Top10Output

class Top10Response(BaseModel):
    data: List[Top10Output]