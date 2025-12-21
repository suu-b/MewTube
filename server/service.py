from math import e
from pinecone import Pinecone
from dotenv import load_dotenv
import json
import os
import logging

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

PINECONE_KEY = os.getenv('PINECONE_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
INDEX_NAME = "mewtube"
DATA_DIR = "./data"


def load_json(path):
    logging.info(f"Loading JSON data from: {path}")
    with open(path, 'r') as f:
        return json.load(f)


def flatten_json(data, source, text_field="projectDescription", id_field="_id"):
    logging.info(f"Flattening data for source: {source}")
    items = []
    for idx, entry in enumerate(data):
        chunk_text = entry.get(text_field, "")
        metadata = {k: v for k, v in entry.items() if k not in [text_field, id_field]}
        items.append({
            "id": entry.get(id_field, f"{source}_{idx}"),
            "chunk_text": chunk_text,
            **metadata
        })
    logging.info(f"Flattened {len(items)} items for source: {source}")
    return items


def main():
    logging.info("Initializing Pinecone client...")
    pc = Pinecone(api_key=PINECONE_KEY)

    if not pc.has_index(INDEX_NAME):
        logging.info(f"Creating Pinecone index: {INDEX_NAME}")
        pc.create_index_for_model(
            name=INDEX_NAME,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "llama-text-embed-v2",
                "field_map": {"text": "chunk_text"}
            }
        )
    else:
        logging.info(f"Index {INDEX_NAME} already exists")

    events_data = load_json(f"{DATA_DIR}/events.json")
    projects_data = load_json(f"{DATA_DIR}/projects.json")

    events_list = events_data.get("sessions", [])
    projects_list = projects_data.get("projects", [])

    events_items = flatten_json(events_list, "event", text_field="videoTitle")
    projects_items = flatten_json(projects_list, "project")

    logging.info(f"Connecting to Pinecone index: {INDEX_NAME}")
    index = pc.Index(host=PINECONE_HOST)

    for namespace, items in [("event", events_items), ("project", projects_items)]:
        logging.info(f"Upserting {len(items)} items to namespace: {namespace}")
        index.upsert_records(namespace, items)
        logging.info(f"Successfully upserted namespace: {namespace}")

    logging.info(f"All data upserted to index: {INDEX_NAME}")


if __name__ == "__main__":
    main()
