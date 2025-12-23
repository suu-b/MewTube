import time
import requests
import logging
from http.client import HTTPException
from itertools import islice

YT_BASE_URL = "https://www.googleapis.com/youtube/v3/search"


class YouTubeSearch:
    """
    Thin wrapper over the YouTube Search API.

    Handles batching, filtering, and aggregation for keyword-based searches.
    """

    def __init__(self, api_key: str, logger: logging.Logger, batch_size: int = 2):
        if not api_key:
            raise ValueError("YouTube API key not found")

        self.api_key = api_key
        self.batch_size = batch_size
        self.logger = logger

    def _batched(self, iterable):
        """Yield iterable in batches of size self.batch_size."""
        self.logger.debug("Batching iterable with batch_size=%d", self.batch_size)

        it = iter(iterable)
        while True:
            batch = list(islice(it, self.batch_size))
            if not batch:
                return
            yield batch

    def _call_api(self, query: str, max_results: int):
        """Call the YouTube Search API and return raw items."""
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

    