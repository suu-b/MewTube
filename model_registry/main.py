from config.config import logger

def register_model(
    client,
    model_name: str,
    version: str, 
    local_path: str,
    bucket: str = 'models',
    status: str = 'active'
):
    """
        Uploads a model artifact on supabase. Does two things:
            1. Stores it in the passed bucket and the passed model name (namespace).
            2. Registers in the model registry
    """

    # Store the model artifact in the bucket
    # We will assume that the bucket and namespace exists
    storage_path = f"{model_name}/{version}/model.joblib"
    with open(local_path, "rb") as f:
        client.storage.from_(bucket).upload(
            storage_path, f, file_options = {"upsert": "false"}
        )
        logger.info("Uploaded model to storage:%s", storage_path)

    # Register the model in the registry
    model_registry_table = client.table("model_versions")
    model_registry_table.insert({
        "model_name": model_name,
        "version": version,
        "storage_bucket": bucket,
        "storage_path": storage_path,
        "status": status
    }).execute()

    logger.info("Registered model in DB: %s v%s", model_name, version)
