from unidecode import unidecode
from re import sub


def normalize_slug(slug: str, default: str) -> str:
    result = sub(
        r"[^a-z0-9]+",
        "-",
        unidecode(slug).lower().strip("-")
    )
    return result or default

