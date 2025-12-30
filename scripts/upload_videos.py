import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client
from huggingface_hub import InferenceClient

from models.video import Video
from config.config import OUTPUT_DIR, VIDEO_TABLE, logger
from util import format_for_embedding


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

VIDEOS_DIR = OUTPUT_DIR / "videos"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

EMBED_BATCH_SIZE = 64        
INSERT_BATCH_SIZE = 500     


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
hf_client = InferenceClient(token=HF_TOKEN)


def load_channel_scores():
    id_to_score = {}

    for layer_file, score in [
        ("layer1.jsonl", 100),
        ("layer2.jsonl", 84),
        ("layer3.jsonl", 54),
    ]:
        path = OUTPUT_DIR / layer_file
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                id_to_score[entry["id"]] = score / 100

    logger.info("Loaded %d channel scores", len(id_to_score))
    return id_to_score


def embed_batch(texts, retries=3):
    for attempt in range(retries):
        try:
            embeddings = hf_client.feature_extraction(
                text=texts,
                model=EMBED_MODEL,
            )

            if isinstance(embeddings[0][0], list):
                embeddings = [e[0] for e in embeddings]

            return embeddings

        except Exception as e:
            if attempt == retries - 1:
                logger.error("Embedding batch failed: %s", e)
                return [[0.0] * 384] * len(texts)

            sleep = 2 ** attempt
            logger.warning("Embedding retry in %ds", sleep)
            time.sleep(sleep)


def stream_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def batched(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch



def main():
    logger.info("Starting video ingestion")

    channel_scores = load_channel_scores()
    insert_buffer = []

    for file_path in VIDEOS_DIR.glob("*.jsonl"):
        logger.info("Processing %s", file_path.name)

        for chunk_idx, video_chunk in enumerate(batched(stream_jsonl(file_path), EMBED_BATCH_SIZE), start=1):
            texts = [
                format_for_embedding(v["title"], v.get("description", ""))
                for v in video_chunk
            ]

            embeddings = embed_batch(texts)

            for video, emb in zip(video_chunk, embeddings):
                insert_buffer.append(
                    Video(
                        **{
                            **video,
                            "embedding": emb,
                            "quality_score": channel_scores.get(video["channel_id"], 0),
                        }
                    ).model_dump(mode = "json")
                )

            if len(insert_buffer) >= INSERT_BATCH_SIZE:
                supabase.table(VIDEO_TABLE).insert(insert_buffer[:INSERT_BATCH_SIZE]).execute()
                logger.info("%s | chunk %d | inserted %d rows", file_path.name, chunk_idx, INSERT_BATCH_SIZE)
                del insert_buffer[:INSERT_BATCH_SIZE]

    if insert_buffer:
        supabase.table(VIDEO_TABLE).insert(insert_buffer).execute()
        logger.info("Inserted final %d rows", len(insert_buffer))

    logger.info("Ingestion complete")


if __name__ == "__main__":
    main()