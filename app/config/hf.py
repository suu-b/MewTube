import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

hf_client = InferenceClient(token=HF_TOKEN)