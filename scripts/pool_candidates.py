from config.config import OUTPUT_DIR, logger
from candidates_service.main import get_candidates
import json
from pathlib import Path

def main():
    print()
    logger.info("Executing Script to pool candidates")
    logger.info("Collecting the candidates...")    
    candidates = get_candidates()
    candidates_found = len(candidates)
    if(candidates_found == 0):
        logger.warning("No candidate found. Exiting...")
        return

    logger.info("Collected %d candidates", candidates_found)
    logger.info("Pooling them (We will append them to a file but not overwrite).")

    # We are using jsonl (JSON Lines) to efficiently append
    with open(OUTPUT_DIR / f"{Path(__file__).stem}_pool.jsonl", "a", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c.model_dump(mode="json"), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()