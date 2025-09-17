from unidecode import unidecode
from re import sub


def normalize_slug(slug: str, default: str) -> str:
    """Приводит строку к виду 'abc-de-f-g' путем
    транслитерации с русского(англ.) на английский
    и отброса специальных символов, убирая их или заменяя на '-'.

    пример:
    'Привет! каК дела?,.' -> 'privet-kak-dela'"""

    result = sub(
        r"[^a-z0-9]+",
        "-",
        unidecode(slug).lower().strip("-")
    )
    return result or default

