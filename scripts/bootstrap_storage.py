from supabase import create_client
from dotenv import load_dotenv
from config.config import logger
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

BUCKET = "models"
MODEL = "candidate_ranker"

client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_bucket_if_not_exists(name: str):
    buckets = client.storage.list_buckets()
    if not any(b["name"] == name for b in buckets):
        logger.warning("Bucket does not exist. Creating: %s", name)
        client.storage.create_bucket(name)
    else:
        logger.info("Bucket already exists: %s", name)


def create_namespace_if_not_exists(model_name: str):
    sentinel_path = f"{model_name}/.keep"
    logger.debug("Sentinel path=%s", sentinel_path)

    client.storage.from_(BUCKET).upload(
        sentinel_path,
        b"",
        file_options={"content-type": "text/plain", "upsert": "True"},
    )

    logger.info("Model namespace ensured: %s", model_name)


def main():
    logger.info("Bucket configured: %s", BUCKET)
    create_bucket_if_not_exists(BUCKET)
    logger.info("Model configured: %s", MODEL)
    create_namespace_if_not_exists(MODEL)
    logger.info("Script executed. Exiting...")


if __name__ == "__main__":
    main()
