import requests
from http.client import HTTPException
from itertools import islice

from config.config import CONTEXT_ENDORSE_KEY, CONTEXT_REJECT_KEY, YT_BASE_URL

class YouTubeSearch:
    def __init__(self, api_key: str, batch_size: int = 2):
        if not api_key:
            raise ValueError("YouTube API key not found")
        self.api_key = api_key
        self.batch_size = batch_size

    def _batched(self, iterable):
        it = iter(iterable)
        while True:
            batch = list(islice(it, self.batch_size))
            if not batch:
                return 
            yield batch                            

    def _call_api(self, query: str, max_results: int):        
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key,
            "regionCode": "US"
        }

        r = requests.get(YT_BASE_URL, params=params)
        if r.status_code != 200:
            raise HTTPException(r.status_code, r.text)

        return r.json().get("items", [])

    def search(self, context: dict, max_results: int = 20):
        results = []
        seen = set()

        endorse = context.get(CONTEXT_ENDORSE_KEY, [])
        reject = context.get(CONTEXT_REJECT_KEY, [])

        for batch in self._batched(endorse):
            query = " ".join(batch)
            items = self._call_api(query, max_results)

            for item in items:
                vid = item["id"]["videoId"]
                text = (
                    item["snippet"]["title"] + " " + 
                    item["snippet"].get("description", "")
                ).lower()

                if(any(r in text for r in reject)):
                    continue

                if vid not in seen:
                    seen.add(vid)
                    results.append(item)

        return results