from config.config import CONTEXT, YT_KEY
from yt_search import YouTubeSearch
import json

yt_search = YouTubeSearch(api_key=YT_KEY)
results = yt_search.search(CONTEXT)
with open("output.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

