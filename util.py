import base64

def format_for_embedding(title: str, description: str) -> str:
    parts = [f"Title: {title.strip()}"]
    if description:
        parts.append(f"Description: {description.strip()}")
    return "\n\n".join(parts)

def decode_video_id(encoded_id: str) -> str:
    return base64.b64decode(encoded_id).decode("utf-8").split('.')[1]
