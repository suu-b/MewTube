def format_for_embedding(title: str, description: str) -> str:
    parts = [f"Title: {title.strip()}"]
    if description:
        parts.append(f"Description: {description.strip()}")
    return "\n\n".join(parts)
