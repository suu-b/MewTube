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
    "introduction to formal logic",
    "thought experiments in philosophy of mind",
    "foundations of epistemology",
    "popper falsifiability explained",
    "critical thinking exercises",
    "turing machine explained step by step",
    "cellular automata simulations",
    "complex systems theory lectures",
    "reinforcement learning projects",
    "bayesian reasoning tutorials",
    "anomaly detection in data science",
    "systems architecture case studies",
    "german romantic poetry readings",
    "early romanticism in literature",
    "anti-enlightenment philosophers",
    "keats negative capability analysis",
    "the sublime in art and literature",
    "visionary mysticism documentaries",
    "william blake illuminated plates",
    "sketching for creative thinking",
    "line drawing exercises",
    "gesture drawing techniques",
    "impressionism structural analysis",
    "unfinished art pieces",
    "draft manuscripts studies",
    "baroque counterpoint tutorials",
    "fugue structure breakdown",
    "beethoven late period analysis",
    "bach fugue performance guide",
    "tchaikovsky composition lectures",
    "theme and variation examples",
    "classic literature explained",
    "modernist literature breakdown",
    "symbolism in poetry analysis",
    "mythology as cognitive framework",
    "writing essays as inquiry",
    "aphorisms in philosophy",
    "first principles thinking exercises",
    "conceptual modeling for reasoning",
    "precision in argumentation",
    "minimalism in art and music"
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



