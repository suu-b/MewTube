import argparse
import os
from dotenv import load_dotenv
from supabase import create_client

from config.config import logger
from model_registry.main import register_model

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    """
        CLI for model registry. Enables a manual run of registration.
    """
    parser = argparse.ArgumentParser(description="Upload a model and register in the model registry")

    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--version", required=True, help="Version string")
    parser.add_argument("--file", required=True, help="Path to artifact")
    parser.add_argument("--status", default="active", choices=["active", "shadow", "deprecated"])
    parser.add_argument("--bucket", default="models", help="Supabase storage bucket")

    args = parser.parse_args()

    logger.info(
    "Executing: model=%s version=%s file=%s bucket=%s status=%s",
    args.model, args.version, args.file, args.bucket, args.status
    )

    register_model(
        client=client,
        model_name=args.model,
        version=args.version,
        local_path=args.file,
        bucket=args.bucket,
        status=args.status
    )

    logger.info("Executed Script. Exiting...")

if __name__ == '__main__':
    main()



