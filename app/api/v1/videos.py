from fastapi import APIRouter, HTTPException
from app.config.db import supabase_client
from config.config import VIDEO_TABLE
from typing import List

from app.service.videos import get_top_10
from models.api.videos.top10_request import Top10Request
from models.api.videos.top10_response import Top10Response

router = APIRouter(prefix="/videos", tags=["videos"])

@router.post("/top10", response_model=Top10Response)
def top10(req: Top10Request):
    return {"data": get_top_10(req.query)}
