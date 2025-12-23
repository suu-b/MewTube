from config.config import logger
from candidates_service.main import get_candidates

def review_candidates(candidates):
    liked = []
    disliked = []

    for i, c in enumerate(candidates, start = 1):
        print("="*60)
        print(f"{i}. Candidate")
        print(f"Video: {c.title}")
        print(c.description or "(no description)")
        print(f"Channel: {c.channel_title}")
        print(f"Published: {c.published_at}")
        print()
        print("=" * 60)

        while True:
            choice = input("0 = dislike/1 = like: ").strip()
            if choice in {"0", "1"}:
                break
            print("Invalid input. Enter 0/1")

        if choice == "1":
            liked.append(c)
        else:
            disliked.append(c)  

    return liked, disliked

def main():
    print()
    logger.info("Executing Script to train the initial model")
    logger.info("Collecting the candidates...")    
    candidates = get_candidates()
    candidates_found = len(candidates)
    if(candidates_found == 0):
        logger.warning("No candidate found. Exiting...")
        return

    logger.info("Collected %d candidates", candidates_found)
    logger.info("Starting Candidates Review.")

    liked, disliked = review_candidates(candidates)
    logger.info(
        "Review complete. Liked: %d | Disliked: %d",
        len(liked),
        len(disliked),
    )

if __name__ == "__main__":
    main()