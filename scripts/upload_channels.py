import os
import json
from models.channel import Channel
from config.config import CHANNEL_TABLE, OUTPUT_DIR, logger
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

layer1 = OUTPUT_DIR / "layer1.jsonl"
layer2 = OUTPUT_DIR / "layer2.jsonl"
layer3 = OUTPUT_DIR / "layer3.jsonl"
 
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

BATCH_SIZE = 500

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

current_hierarchy = f"""Current Hierarchy:
channel_score: 85-100 : layer1
channel_score: 55-84 : layer2
channel_score: 1-54: layer3"""

def push_to_supabase(layer, channel_score):
    logger.info("Pushing %s channels to supabase", layer)
    with open(layer, "r", encoding="utf-8") as f:
        channels = [Channel(**{**json.loads(line), "channel_score": channel_score}) for line in f]

    logger.debug("Parsed %d channels", len(channels))

    for i in range(0, len(channels), BATCH_SIZE):
        batch = [c.model_dump() for c in channels[i:i+BATCH_SIZE]]
        try:
            res = supabase.table(CHANNEL_TABLE).insert(batch).execute()
            logger.info("Inserted batch %d-%d: %d rows", i+1, i+len(batch), len(res.data or []))
        except Exception as e:
            logger.error("Failed to insert batch %d-%d: %s", i+1, i+len(batch), e)

def main():
    logger.info("Executing Upload channels script...")
    logger.info(current_hierarchy)
    logger.debug("Paths:")
    logger.debug("For layer 1: %s", layer1)
    logger.debug("For layer 2: %s", layer2)
    logger.debug("For layer 3: %s", layer3)

    push_to_supabase(layer1, 100)
    push_to_supabase(layer2, 84)
    push_to_supabase(layer3, 54)
    
    logger.info("Script executed successfully!")


if __name__ == '__main__':
    main()
