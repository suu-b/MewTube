from typing import List
from decimal import Decimal
import numpy as np

from config.config import logger, SIMILARITY_WEIGHT, CHANNEL_WEIGHT
from app.config.db import supabase_client
from app.config.hf import hf_client, EMBED_MODEL
from models.api.videos.top10_output import Top10Output


def calculate_score(r: Top10Output) -> Decimal:
    """
    Final ranking score.
    Similarity carries 70% weight, channel score carries 20%.
    Remaining weight is intentionally unused for future signals.
    """
    return (
        SIMILARITY_WEIGHT * Decimal(r.similarity)
        + CHANNEL_WEIGHT * Decimal(r.channel_score)
    )


def get_top_10(query: str) -> List[Top10Output]:
    logger.info("Query: %s", query)

    embedding = hf_client.feature_extraction(
        text=query,
        model=EMBED_MODEL
    )

    if isinstance(embedding, np.ndarray):
        vector = embedding.astype(float).tolist()
    elif isinstance(embedding, list):
        if isinstance(embedding[0], list):
            vector = [float(x) for x in embedding[0]]
        else:
            vector = [float(x) for x in embedding]
    else:
        raise TypeError(f"Unexpected embedding type: {type(embedding)}")

    resp = supabase_client.rpc(
        "search_videos",
        {"q": vector, "k": 50}
    ).execute()

    if not resp.data:
        logger.warning("No results returned from vector search")
        return []

    rows: List[Top10Output] = [
        Top10Output.model_validate(r) for r in resp.data
    ]

    ranked = sorted(rows, key=calculate_score, reverse=True)
    return ranked[:10]
