from pathlib import Path
from config.config import OUTPUT_DIR, logger
from models.candidate import Candidate 
from .youtube_search import YouTubeSearch
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

YT_KEY = os.getenv("YT_KEY")

# Sample context
CONTEXT = {
    "endorse": {
    "philosophy video essays",
    "scientific debate",
    "philosophy debate",
    "thought experiment",
    "close reading literature",
    "adam walker unsolicited advice",
    "line by line literature",
    "english poem recitation",
    "philosophy of computer science",
    "theoretical computer science",
    "vintage documentaries",
    "cinema",
    "poetics",
    "painting"
},
    "reject": {
        "tutorial",
        "course",
        "short",
    },
}

def to_candidate(result) -> Candidate:
    snippet = result["snippet"]
    return Candidate(
        video_id=result["id"]["videoId"],
        title=snippet["title"],
        description=snippet.get("description"),
        channel_id=snippet["channelId"],
        channel_title=snippet["channelTitle"],
        published_at=snippet["publishedAt"],
        fetched_at=datetime.utcnow(),
        thumbnail_url=snippet["thumbnails"]["medium"]["url"],
    )

def get_candidates():
    logger.info("Initializing Youtube Search Object")

    yt_search = YouTubeSearch(api_key=YT_KEY, logger=logger) 
    logger.info("Initialized Youtube Search Object")

    results = yt_search.search(CONTEXT)

    logger.info("Parsing the results into pydantic models...")

    # To test the youtube api by dumping in some local file. See output.json for sample out
    # with open(OUTPUT_DIR / f"{Path(__file__).stem}_ytsearch.json", "w") as f:
    #     json.dump(results, f, indent=2, ensure_ascii=False)

    candidates = [to_candidate(r) for r in results]
    logger.info("Converted the models successfully (candidates length=%d)", len(candidates))
    logger.info("Returning execution back to the caller")
    return candidates

def main():
    logger.info("Starting Candidates Service...")
    candidates = get_candidates()
    # To test the pydantic model for candidates.
    # with open(OUTPUT_DIR / f"{Path(__file__).stem}_candidates.json", "w") as f:
    #     json.dump(
    #         [c.model_dump(mode="json") for c in candidates[:20]],
    #         f,
    #         indent=2,
    #         ensure_ascii=False
    #     )

if __name__ == '__main__':
    main()



