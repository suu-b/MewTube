import logging
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Inner Configurations
_isNonProd = os.getenv('IS_NON_PROD', 'true').lower() == 'true'

# Shared Constants
LOGGING_LEVEL = logging.DEBUG if _isNonProd else logging.INFO
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Shared Logger
logger = logging.getLogger('mewtube')
logger.setLevel(LOGGING_LEVEL)

if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
