import logging
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Inner Configurations
_isNonProd = os.getenv('IS_NON_PROD', 'true').lower() == 'true'

# Shared Constants
APP_NAME = "MewTube"
LOGGING_LEVEL = logging.DEBUG if _isNonProd else logging.INFO
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Table names
CHANNEL_TABLE = "channels"
VIDEO_TABLE = "videos"

# Shared Logger
logger = logging.getLogger(APP_NAME)
logger.setLevel(LOGGING_LEVEL)

if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
