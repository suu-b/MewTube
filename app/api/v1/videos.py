from fastapi import APIRouter, HTTPException
from app.config.db import supabase_client
from config.config import VIDEO_TABLE

router = APIRouter(prefix="/videos", tags=["videos"])

@router.get("/unsolicited_advice")
def home():
    response = supabase_client.table(VIDEO_TABLE).select("*").eq("channel_id", "UCW71hQg1kDxmFIfijA8dL0Q").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="No videos found")

    return response.data
