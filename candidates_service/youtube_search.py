import time
import requests
import logging
from http.client import HTTPException

YT_BASE_URL = "https://www.googleapis.com/youtube/v3/search"


class YouTubeSearch:
    """
    Thin wrapper over the YouTube Search API.

    Runs one search per endorse term with hard negative filtering.
    """

    def __init__(self, api_key: str, logger: logging.Logger):
        if not api_key:
            raise ValueError("YouTube API key not found")

        self.api_key = api_key
        self.logger = logger

    def _build_query(self, endorse: str, reject: list[str]) -> str:
        negative = " ".join(f"-{term}" for term in reject)
        return f"{endorse} {negative}".strip()

    def _call_api(self, query: str, max_results: int):
        self.logger.debug(
            "Calling YouTube API with query=%s max_results=%d",
            query,
            max_results,
        )

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key,
            "regionCode": "US",
        }

        r = requests.get(YT_BASE_URL, params=params, timeout=10)

        if r.status_code != 200:
            self.logger.error(
                "YouTube API call failed",
                extra={
                    "status_code": r.status_code,
                    "query": query,
                    "response": r.text,
                },
            )
            raise HTTPException(r.status_code, r.text)

        return r.json().get("items", [])

    def search(self, context: dict, max_results: int = 30):
        """
        Run independent searches for each endorse term.

        Returns a deduplicated list of video items.
        """
        start = time.monotonic()

        endorse = context.get("endorse", [])
        reject = context.get("reject", [])

        self.logger.info(
            "YouTube search started (endorse=%d reject=%d)",
            len(endorse),
            len(reject),
        )

        results = []
        seen = set()

        for term in endorse:
            query = self._build_query(term, reject)
            items = self._call_api(query, max_results)

            for item in items:
                vid = item["id"]["videoId"]
                if vid not in seen:
                    seen.add(vid)
                    results.append(item)

            time.sleep(1)  # rate-limit hygiene

        duration = time.monotonic() - start

        self.logger.info(
            "YouTube search completed (results=%d duration=%.2fs)",
            len(results),
            duration,
        )

        return results
