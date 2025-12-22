import logging
from config.config import logger
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
        "philosophy",
        "formal logic",
        "philosophy of mind",
        "epistemology",
        "critical rationalism",
        "computation",
        "turing machine",
        "automata theory",
        "complex systems",
        "reinforcement learning",
        "probabilistic reasoning",
        "anomaly detection",
        "systems design",
        "romanticism (late)",
        "proto-romanticism",
        "anti-enlightenment thought",
        "negative capability",
        "the sublime",
        "visionary mysticism (non-theological)",
        "william blake",
        "sketching as thinking",
        "line over color",
        "gesture drawing",
        "impressionism (structural, not decorative)",
        "unfinished form",
        "drafts and marginalia",
        "western classical music",
        "counterpoint",
        "fugue",
        "late beethoven",
        "bach (structural reading)",
        "tchaikovsky",
        "theme and variation",
        "classic literature",
        "modernist fragmentation",
        "symbolism (austere)",
        "myth as cognitive scaffold",
        "essay as inquiry",
        "aphoristic prose",
        "first principles",
        "model-based thinking",
        "precision over eloquence",
        "minimalism",
    },
    "reject": {
        "tutorial",
        "hand-holding",
        "survey courses",
        "buzzwords",
        "cargo-cult ai",
        "overengineering",
        "romantic nostalgia",
        "aestheticized vagueness",
        "poetic obscurity",
        "motivational fluff",
        "linkedin prose",
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

def main():
    logger.info("Starting Candidates Service...")
    logger.info("Initializing Youtube Search Object")

    yt_search = YouTubeSearch(api_key=YT_KEY, logger=logger) 
    logger.info("Initialized Youtube Search Object")

    results = yt_search.search(CONTEXT)

    logger.info("Parsing the results into pydantic models...")

    # To test the youtube api by dumping in some local file. See output.json for sample out
    # with open("output.json", "w") as f:
    #     json.dump(results, f, indent=2, ensure_ascii=False)

    candidates = [to_candidate(r) for r in results]

    logger.info("Converted the models successfully (candidates length=%d)", len(candidates))

    # To test the pydantic model for candidates.
    # with open("candidates.json", "w") as f:
    #     json.dump(
    #         [c.model_dump(mode="json") for c in candidates[:20]],
    #         f,
    #         indent=2,
    #         ensure_ascii=False
    #     )

    logger.info("Returning execution back to the caller")
    return candidates

if __name__ == '__main__':
    main()



